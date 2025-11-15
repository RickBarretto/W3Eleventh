const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Rewards (claim tests)", function () {
    let Game, game, host, guest;

    beforeEach(async function () {
        [, host, guest] = await ethers.getSigners();

        Game = await ethers.getContractFactory("CardGame");
        game = await Game.deploy();

        await game.deployed();
    });

    it("allows winner to claim reward and mints a card", async function () {
        const hostsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(host.address, "Striker", 90)
        );
        
        const guestsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(guest.address, "Defender", 70)
        );
        
        await game.conductMatchBetween(hostsCard, guestsCard);
        expect(await rewardCount(game, host.address)).to.equal(1);

        const newId = await claimReward(game, host);
        expect(await cardCount(game, host.address)).to.be.greaterThan(1);
        expect(await rewardCount(game, host.address)).to.equal(0);

        const cardInfo = await game.cardDetails(newId);
        expect(cardInfo[2]).to.equal(host.address);
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

