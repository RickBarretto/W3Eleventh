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
    const a = player1.address;
    const b = player2.address;
    const tx1 = await cardGame.awardUniqueCardTo(a, "Striker", 90);
    const rc1 = await tx1.wait();
    const id1 = rc1.events.find((e) => e.event === 'CardWasAwarded').args.cardId.toNumber();

    const tx2 = await cardGame.awardUniqueCardTo(b, "Defender", 70);
    const rc2 = await tx2.wait();
    const id2 = rc2.events.find((e) => e.event === 'CardWasAwarded').args.cardId.toNumber();

    await cardGame.conductMatchBetween(id1, id2);
    expect((await cardGame.pendingRewardCountFor(a)).toNumber()).to.equal(1);
    expect((await cardGame.pendingRewardCountFor(b)).toNumber()).to.equal(0);
  });

  it("does not award pending reward on draw", async function () {
    const a = player1.address;
    const b = player2.address;
    const tx3 = await cardGame.awardUniqueCardTo(a, "Mid", 80);
    const id3 = (await tx3.wait()).events.find((e) => e.event === 'CardWasAwarded').args.cardId.toNumber();
    const tx4 = await cardGame.awardUniqueCardTo(b, "Mid", 80);
    const id4 = (await tx4.wait()).events.find((e) => e.event === 'CardWasAwarded').args.cardId.toNumber();

    await cardGame.conductMatchBetween(id3, id4);
    expect((await cardGame.pendingRewardCountFor(a)).toNumber()).to.equal(0);
    expect((await cardGame.pendingRewardCountFor(b)).toNumber()).to.equal(0);
  });
});
