// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract CardGame {

    struct Card {
        string name;
        uint256 power;
        address owner;
    }

    uint256 public lastCardID;
    mapping(address => bool) private teamExists;

    mapping(uint256 => Card) public cards;
    mapping(address => uint256[]) private teams;
    mapping(address => uint256) private pendingRewards;

    event TeamWasCreated(address indexed player);
    event CardWasAwarded(uint256 indexed cardId, address indexed to, string name, uint256 power);
    event RewardNowAvailable(address indexed player, uint256 amount);
    event RewardWasClaimed(address indexed player, uint256 indexed cardId);

    // Create a new team for `player`. If it's a new team, grant 5 starter cards.
    function createNewTeamFor(address player) external {
        if (!teamExists[player]) {
            teamExists[player] = true;
            emit TeamWasCreated(player);

            // grant 5 starter cards with readable names
            for (uint256 i = 0; i < 5; i++) {
                string memory name = string(abi.encodePacked("Starter #", _uintToString(i + 1)));
                _awardCard(player, name, 50 + i); // incremental power 50..54
            }
        }
    }

    // Returns true when the player already has a team
    function doesTeamExist(address player) external view returns (bool) {
        return teamExists[player];
    }

    // Returns the number of cards currently in the player's team
    function numberOfCardsInTeam(address player) external view returns (uint256) {
        return teams[player].length;
    }

    // Reward a new unique card to `to` with given name and power. Returns card id.
    // Award a uniquely identified card to `to` with given name and power.
    function awardUniqueCardTo(address to, string calldata name, uint256 power) external returns (uint256) {
        return _awardCard(to, name, power);
    }

    function _awardCard(address to, string memory name, uint256 power) internal returns (uint256) {
        lastCardID += 1;
        uint256 id = lastCardID;

        cards[id] = Card({name: name, power: power, owner: to});
        teams[to].push(id);
        teamExists[to] = true;
        emit CardWasAwarded(id, to, name, power);

        return id;
    }

    // How many unclaimed match-win rewards does `player` have?
    function pendingRewardCountFor(address player) external view returns (uint256) {
        return pendingRewards[player];
    }

    // Read card details (name, power, owner) for a given card id
    function cardDetails(uint256 id) external view returns (string memory, uint256, address) {
        Card memory c = cards[id];
        return (c.name, c.power, c.owner);
    }

    // Play a match between card `a` and `b`. Returns winner card id (0 for draw) and powers.
    // NOTE: this function now records a pending reward for the owner of the winning card.
    // Conduct a match between two card ids. Records a pending reward for the winner's owner.
    function conductMatchBetween(uint256 a, uint256 b) external returns (uint256 winnerId, uint256 aPower, uint256 bPower) {
        require(a != 0 && b != 0, "invalid card id");

        aPower = cards[a].power;
        bPower = cards[b].power;

        if (aPower > bPower) {
            winnerId = a;
            address winner = cards[a].owner;
            pendingRewards[winner] += 1;
            emit RewardNowAvailable(winner, pendingRewards[winner]);
        } else if (bPower > aPower) {
            winnerId = b;
            address winner = cards[b].owner;
            pendingRewards[winner] += 1;
            emit RewardNowAvailable(winner, pendingRewards[winner]);
        } else {
            winnerId = 0;
        }
    
    }

    // Claim a single pending reward and receive a new card.
    // Claim a single pending reward and receive a new card.
    function claimPendingReward() external returns (uint256) {
        uint256 pending = pendingRewards[msg.sender];
        require(pending > 0, "no pending rewards");

        pendingRewards[msg.sender] = pending - 1;

        // mint a reward card with readable name
        uint256 id = _awardCard(
            msg.sender, 
            string(abi.encodePacked("Reward #", _uintToString(rewardIndexFor(msg.sender)))), 
            60
        );
        emit RewardWasClaimed(msg.sender, id);
        return id;

    }

    // helper to compute a small index for reward naming (team size + 1)
    // Compute an index for reward naming (current team size + 1)
    function rewardIndexFor(address player) internal view returns (uint256) {
        return teams[player].length + 1;
    }

    // simple uint -> string helper
    function _uintToString(uint256 value) internal pure returns (string memory) {
        if (value == 0) { return "0"; }

        uint256 temp = value;
        uint256 digits;

        while (temp != 0) {
            digits++;
            temp /= 10;
        }

        bytes memory buffer = new bytes(digits);

        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }

        return string(buffer);
    }
}
