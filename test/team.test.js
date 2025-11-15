const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TeamManager (team tests)", function () {
  let CardGame, cardGame, player;

  beforeEach(async function () {
    [, player] = await ethers.getSigners();
    CardGame = await ethers.getContractFactory("CardGame");
    cardGame = await CardGame.deploy();
    await cardGame.deployed();
  });

  it("creates a team and grants 5 starter cards", async function () {
    const p = player.address;
    await cardGame.createNewTeamFor(p);
    expect(await cardGame.doesTeamExist(p)).to.equal(true);
    expect((await cardGame.numberOfCardsInTeam(p)).toNumber()).to.equal(5);

    // idempotent
    await cardGame.createNewTeamFor(p);
    expect((await cardGame.numberOfCardsInTeam(p)).toNumber()).to.equal(5);
  });
});
