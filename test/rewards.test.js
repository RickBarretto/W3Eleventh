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
        const a = player1.address;
        const b = player2.address;
        const tx1 = await cardGame.awardUniqueCardTo(a, "Striker", 90);
        const id1 = (await tx1.wait()).events.find((e) => e.event === 'CardWasAwarded').args.cardId.toNumber();
        const tx2 = await cardGame.awardUniqueCardTo(b, "Defender", 70);
        const id2 = (await tx2.wait()).events.find((e) => e.event === 'CardWasAwarded').args.cardId.toNumber();

        await cardGame.conductMatchBetween(id1, id2);
        expect((await cardGame.pendingRewardCountFor(a)).toNumber()).to.equal(1);

        const claimTx = await cardGame.connect(player1).claimPendingReward();
        const rc = await claimTx.wait();
        const ev = rc.events.find((e) => e.event === 'RewardWasClaimed');
        const newId = ev.args.cardId.toNumber();
        // team card count increased
        expect((await cardGame.numberOfCardsInTeam(a)).toNumber()).to.be.greaterThan(1);
        // pending rewards decremented
        expect((await cardGame.pendingRewardCountFor(a)).toNumber()).to.equal(0);

        const card = await cardGame.cardDetails(newId);
        expect(card[2]).to.equal(a);
    });
});
