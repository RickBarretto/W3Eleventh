const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("CardStore (card tests)", function () {
  let CardGame, cardGame, owner, player;

  beforeEach(async function () {
    [owner, player] = await ethers.getSigners();
    CardGame = await ethers.getContractFactory("CardGame");
    cardGame = await CardGame.deploy();
    await cardGame.deployed();
  });

  it("rewards unique cards and stores attributes", async function () {
    const p = player.address;
    const tx1 = await cardGame.awardUniqueCardTo(p, "Defender", 70);
    const rc1 = await tx1.wait();
    const ev1 = rc1.events.find((e) => e.event === 'CardWasAwarded');
    const id1 = ev1.args.cardId.toNumber();
    const card1 = await cardGame.cardDetails(id1);
    expect(card1[0]).to.equal("Defender");
    expect(card1[1].toNumber()).to.equal(70);
    expect(card1[2]).to.equal(p);

    const tx2 = await cardGame.awardUniqueCardTo(p, "Defender", 70);
    const rc2 = await tx2.wait();
    const ev2 = rc2.events.find((e) => e.event === 'CardWasAwarded');
    const id2 = ev2.args.cardId.toNumber();
    expect(id1).to.not.equal(id2);
    expect((await cardGame.numberOfCardsInTeam(p)).toNumber()).to.equal(2);
  });
});
