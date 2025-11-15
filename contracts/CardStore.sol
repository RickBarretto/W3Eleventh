// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract CardStore {
    struct Card {
        string name;
        uint256 power;
        address owner;
    }

    uint256 public nextCardId;
    mapping(uint256 => Card) public cards;

    function createCard(address to, string calldata name, uint256 power) external returns (uint256) {
        nextCardId += 1;
        uint256 id = nextCardId;
        cards[id] = Card({name: name, power: power, owner: to});
        return id;
    }

    function getCard(uint256 id) external view returns (string memory, uint256, address) {
        Card memory c = cards[id];
        return (c.name, c.power, c.owner);
    }
}
