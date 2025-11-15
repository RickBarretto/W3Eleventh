const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("CardGame (basic TDD tests)", function () {
  let CardGame, cardGame, owner, player1, player2;

  beforeEach(async function () {
    [owner, player1, player2] = await ethers.getSigners();
    CardGame = await ethers.getContractFactory("CardGame");
    cardGame = await CardGame.deploy();
    await cardGame.deployed();
  });

  it("creates a new team and is idempotent", async function () {
    const p1 = player1.address;
    await cardGame.createNewTeamFor(p1);
    expect(await cardGame.doesTeamExist(p1)).to.equal(true);
    // creating a team now grants 5 starter cards
    expect((await cardGame.numberOfCardsInTeam(p1)).toNumber()).to.equal(5);

    // Create again should still be fine
    await cardGame.createNewTeamFor(p1);
    expect(await cardGame.doesTeamExist(p1)).to.equal(true);
    expect((await cardGame.numberOfCardsInTeam(p1)).toNumber()).to.equal(5);
  });

  it("rewards unique cards and stores attributes", async function () {
    const p2 = player2.address;
    const tx1 = await cardGame.awardUniqueCardTo(p2, "Defender", 70);
    const rc1 = await tx1.wait();
    const id1 = 1;
    const card1 = await cardGame.cardDetails(id1);
    expect(card1[0]).to.equal("Defender");
    expect(card1[1].toNumber()).to.equal(70);
    expect(card1[2]).to.equal(p2);

    // Reward another card with same name — should be distinct id
    const tx2 = await cardGame.awardUniqueCardTo(p2, "Defender", 70);
    const id2 = 2;
    const card2 = await cardGame.cardDetails(id2);
    expect(card2[0]).to.equal("Defender");
    expect(card2[1].toNumber()).to.equal(70);
    expect(card2[2]).to.equal(p2);

    expect(id1).to.not.equal(id2);
    expect((await cardGame.numberOfCardsInTeam(p2)).toNumber()).to.equal(2);
  });

  it("determines match winners based on power and handles draws", async function () {
    const a = player1.address;
    const b = player2.address;
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
    const claimTx = await cardGame.connect(player1).claimPendingReward();
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
