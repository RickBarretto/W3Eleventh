const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Rewards (claim tests)", function () {
    let CardGame, cardGame, player1, player2;

    beforeEach(async function () {
        [, player1, player2] = await ethers.getSigners();

        CardGame = await ethers.getContractFactory("CardGame");
        cardGame = await CardGame.deploy();

        await cardGame.deployed();
    });

    it("allows winner to claim reward and mints a card", async function () {
        const host = player1.address;
        const guest = player2.address;

        const hostsCard = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(host, "Striker", 90)
        );
        
        const guestsCard = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(guest, "Defender", 70)
        );
        
        await cardGame.conductMatchBetween(hostsCard, guestsCard);
        expect(await rewardCount(cardGame, host)).to.equal(1);

        const newId = await claimReward(cardGame, player1);
        expect(await cardCount(cardGame, host)).to.be.greaterThan(1);
        expect(await rewardCount(cardGame, host)).to.equal(0);

        const cardInfo = await cardGame.cardDetails(newId);
        expect(cardInfo[2]).to.equal(host);
    });
});

async function cardIdFromTransaction(tx1) {
    return (await tx1.wait())
        .events
        .find((e) => e.event === 'CardWasAwarded')
        .args
        .cardId
        .toNumber();
}

async function claimReward(cardGame, player1) {
    const claimTx = await cardGame.connect(player1).claimPendingReward();
    const rc = await claimTx.wait();
    const ev = rc.events.find((e) => e.event === 'RewardWasClaimed');
    const newId = ev.args.cardId.toNumber();
    return newId;
}

async function rewardCount(cardGame, a) {
    return (await cardGame.pendingRewardCountFor(a)).toNumber();
}

async function cardCount(cardGame, a) {
    return (await cardGame.numberOfCardsInTeam(a)).toNumber();
}

