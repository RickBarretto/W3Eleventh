const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("MatchEngine (match tests)", function () {
    let CardGame, cardGame, player1, player2;

    beforeEach(async function () {
        [, player1, player2] = await ethers.getSigners();
        CardGame = await ethers.getContractFactory("CardGame");
        cardGame = await CardGame.deploy();
        await cardGame.deployed();
    });

    it("awards pending reward to winning card owner", async function () {
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
        expect(await rewardCount(cardGame, guest)).to.equal(0);
    });

    it("does not award pending reward on draw", async function () {
        const host = player1.address;
        const guest = player2.address;

        const hostsCard = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(host, "Mid", 80)
        );

        const guestsCard = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(guest, "Mid", 80)
        );

        await cardGame.conductMatchBetween(hostsCard, guestsCard);
        expect(await rewardCount(cardGame, host)).to.equal(0);
        expect(await rewardCount(cardGame, guest)).to.equal(0);
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

async function rewardCount(cardGame, a) {
    return (await cardGame.pendingRewardCountFor(a)).toNumber();
}
