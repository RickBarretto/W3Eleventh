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
        const playerAddress = player.address;

        const claimTransaction = await cardGame.awardUniqueCardTo(playerAddress, "Defender", 70);
        const transactionReceipt = await claimTransaction.wait();

        const claimedCardEvent = transactionReceipt.events.find((e) => e.event === 'CardWasAwarded');
        const cardIdNumber = claimedCardEvent.args.cardId.toNumber();
        const cardInfo = await cardGame.cardDetails(cardIdNumber);

        expect(cardInfo[0]).to.equal("Defender");
        expect(cardInfo[1].toNumber()).to.equal(70);
        expect(cardInfo[2]).to.equal(playerAddress);


        const claimTransaction2 = await cardGame.awardUniqueCardTo(playerAddress, "Defender", 70);
        const transactionReceipt2 = await claimTransaction2.wait();
        const claimedCardEvent2 = transactionReceipt2.events.find((e) => e.event === 'CardWasAwarded');
        const cardIdNumber2 = claimedCardEvent2.args.cardId.toNumber();

        expect(cardIdNumber).to.not.equal(cardIdNumber2);
        expect((await cardGame.numberOfCardsInTeam(playerAddress)).toNumber()).to.equal(2);

    });
});
