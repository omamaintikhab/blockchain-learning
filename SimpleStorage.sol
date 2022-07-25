// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage{
uint256 public favouriteNumber;
function store(uint256 _favouriteNumber) public{
    favouriteNumber=_favouriteNumber;
}
function retrieve() public view returns(uint256){
    return favouriteNumber;
}

struct People {
    uint256 favouriteNumber;
    string name;
}
 People[] public people;
 mapping (string => uint256) public nameToFavouriteNumber;

function addPerson(string memory _name, uint256 _favouriteNumber) public {
    people.push(People(_favouriteNumber,_name));
    nameToFavouriteNumber[_name]=_favouriteNumber;
}
// // People public person = People({favouriteNumber: 24,name: 'omama'});
// function store(uint256 _favouriteNumber)public{
//  favouriteNumber=_favouriteNumber;
//  uint256 test =4;

// }

}