const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("CardGame (basic TDD tests)", function () {
    let CardGame, cardGame, owner, host, guest;

    beforeEach(async function () {
        [owner, host, guest] = await ethers.getSigners();

        CardGame = await ethers.getContractFactory("CardGame");
        cardGame = await CardGame.deploy();

        await cardGame.deployed();
    });

    it("creates a new team and is idempotent", async function () {
        const hostAddress = host.address;
        await cardGame.createNewTeamFor(hostAddress);
    
        expect(await hasTeam(cardGame, hostAddress)).to.equal(true);
        expect(await cardCount(cardGame, hostAddress)).to.equal(5);

        await cardGame.createNewTeamFor(hostAddress);
        expect(await hasTeam(cardGame, hostAddress)).to.equal(true);
        expect(await cardCount(cardGame, hostAddress)).to.equal(5);
    });

    it("rewards unique cards and stores attributes", async function () {
        const guestAddress = guest.address;
        const guestsCardId = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(guestAddress, "Defender", 70)
        );
        const guestCard = await cardGame.cardDetails(guestsCardId);
    
        expect(guestCard[0]).to.equal("Defender");
        expect(guestCard[1].toNumber()).to.equal(70);
        expect(guestCard[2]).to.equal(guestAddress);

        const guestsCardId2 = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(guestAddress, "Defender", 70)
        );
        const guestCard2 = await cardGame.cardDetails(guestsCardId2);

        expect(guestCard2[0]).to.equal("Defender");
        expect(guestCard2[1].toNumber()).to.equal(70);
        expect(guestCard2[2]).to.equal(guestAddress);

        expect(guestsCardId).to.not.equal(guestsCardId2);
        expect(await cardCount(cardGame, guestAddress)).to.equal(2);
    });

    it("determines match winners based on power and handles draws", async function () {
        const a = host.address;
        const b = guest.address;
        // Reward two cards: id 1 -> power 90 to p1, id 2 -> power 70 to p2
        const txA = await cardGame.awardUniqueCardTo(a, "Striker", 90);
        const idA = (await txA.wait()).events.find((e) => e.event === 'CardWasAwarded').args.cardId.toNumber();
        const txB = await cardGame.awardUniqueCardTo(b, "Defender", 70);
        const idB = (await txB.wait()).events.find((e) => e.event === 'CardWasAwarded').args.cardId.toNumber();

        // play the match (state-changing) so pending reward is recorded
        await cardGame.conductMatchBetween(idA, idB);
        // winner's owner (player1) should have one pending reward
        expect((await cardGame.pendingRewardCountFor(a)).toNumber()).to.equal(1);

        // claim the reward as player1 and capture the claimed card id
        const claimTx = await cardGame.connect(host).claimPendingReward();
        const claimRc = await claimTx.wait();
        const rewardEvent = claimRc.events.find((e) => e.event === 'RewardWasClaimed');
        const claimedId = rewardEvent.args.cardId.toNumber();
        // after claiming, team card count increments by 1
        expect((await cardGame.numberOfCardsInTeam(a)).toNumber()).to.equal(2);

        // Draw case: reward two equal-power cards and use their emitted ids
        const tx3 = await cardGame.awardUniqueCardTo(a, "Mid", 80);
        const rc3 = await tx3.wait();
        const ev3 = rc3.events.find((e) => e.event === 'CardWasAwarded');
        const id3 = ev3.args.cardId.toNumber();

        const tx4 = await cardGame.awardUniqueCardTo(b, "Mid", 80);
        const rc4 = await tx4.wait();
        const ev4 = rc4.events.find((e) => e.event === 'CardWasAwarded');
        const id4 = ev4.args.cardId.toNumber();

        const tx = await cardGame.conductMatchBetween(id3, id4);
        await tx.wait();
        // draw should not create pending rewards for player1
        expect((await cardGame.pendingRewardCountFor(a)).toNumber()).to.equal(0);
    });
});

async function hasTeam(cardGame, hostAddress) {
    return await cardGame.doesTeamExist(hostAddress);
}

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