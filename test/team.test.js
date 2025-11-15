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
        const playerAddress = player.address;

        await cardGame.createNewTeamFor(playerAddress);
        expect(await cardGame.doesTeamExist(playerAddress)).to.equal(true);
        expect(await countCards(cardGame, playerAddress)).to.equal(5);

        await cardGame.createNewTeamFor(playerAddress);
        expect(await countCards(cardGame, playerAddress)).to.equal(5);
    });
});

async function countCards(cardGame, playerAddress) {
    return (await cardGame.numberOfCardsInTeam(playerAddress)).toNumber();
}

