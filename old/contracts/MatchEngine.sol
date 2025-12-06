// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract MatchEngine {
    // Returns 0 for draw, 1 when first wins, 2 when second wins
    function compare(uint256 aPower, uint256 bPower) external pure returns (uint8) {
        if (aPower > bPower) return 1;
        if (bPower > aPower) return 2;
        return 0;
    }
}
