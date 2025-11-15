const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("TeamManager (team tests)", function () {
    let Game, game, player;

    beforeEach(async function () {
        [, player] = await ethers.getSigners();

        Game = await ethers.getContractFactory("CardGame");
        game = await Game.deploy();

        await game.deployed();
    });

    it("creates a team and grants 5 starter cards", async function () {
        const playerAddress = player.address;

        await game.createNewTeamFor(playerAddress);
        expect(await game.doesTeamExist(playerAddress)).to.equal(true);
        expect(await countCards(game, playerAddress)).to.equal(5);

        await game.createNewTeamFor(playerAddress);
        expect(await countCards(game, playerAddress)).to.equal(5);
    });
});

async function countCards(cardGame, playerAddress) {
    return (await cardGame.numberOfCardsInTeam(playerAddress)).toNumber();
}

