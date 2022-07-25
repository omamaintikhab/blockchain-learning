import json
from web3 import Web3
from solcx import compile_standard, install_solc
with open('./SimpleStorage.sol', 'r') as file:
    simple_storage_file = file.read()
    
install_solc("0.6.0")
# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open('compiled_code.json', 'w') as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
# chain_id = 4
#
# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0xc75E148Db5a2Fb82054FD940ef63f89486FDb39b"
'''
when adding private key in python always add 0x in front
'''
private_key = "0xa5a9b7ae175efebca19154e418b20f4838f8ac1ef50e0730d5dbc0d1d6a854dd"

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

print(SimpleStorage)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)
# 1. build a transaction
# 2. sign a transaction
# 3. send a transaction
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

#print(transaction)

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
#print(signed_txn)

# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

#working with the contract you always need 
# 1. contract address
# 2. abi
# Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

#get initial value of favourite number
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

'''
making transaction in the blockchain there are two different way we can interact
we can interact with CALL , we can interact with TRANSACT
Call => Simulate making a call and getting a return valu
Transact => where state changes takes place
'''
print('updating contract...')
store_transaction = simple_storage.functions.store(17).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_stored_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

tx_store_hash = w3.eth.send_raw_transaction(signed_stored_txn.rawTransaction)
print("Updated stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_store_hash)

print(f"After transaction is made Stored Value {simple_storage.functions.retrieve().call()}")