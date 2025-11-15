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
        const host = player.address;

        const cardIdNumber = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(host, "Defender", 70)
        );
        const cardInfo = await cardGame.cardDetails(cardIdNumber);

        expect(cardInfo[0]).to.equal("Defender");
        expect(cardInfo[1].toNumber()).to.equal(70);
        expect(cardInfo[2]).to.equal(host);


        const cardIdNumber2 = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(host, "Defender", 70)
        );

        expect(cardIdNumber).to.not.equal(cardIdNumber2);
        expect(await cardCount(cardGame, host)).to.equal(2);

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

async function cardCount(cardGame, a) {
    return (await cardGame.numberOfCardsInTeam(a)).toNumber();
}