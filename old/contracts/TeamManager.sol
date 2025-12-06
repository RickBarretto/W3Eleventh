// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract TeamManager {
    mapping(address => uint256[]) private teams;
    mapping(address => bool) private hasTeam;

    event TeamCreated(address indexed player);

    function createTeam(address player) external {
        if (!hasTeam[player]) {
            hasTeam[player] = true;
            emit TeamCreated(player);
        }
    }

    function teamExists(address player) external view returns (bool) {
        return hasTeam[player];
    }

    function teamCardCount(address player) external view returns (uint256) {
        return teams[player].length;
    }

    function addCardToTeam(address player, uint256 cardId) external {
        teams[player].push(cardId);
        hasTeam[player] = true;
    }
}
