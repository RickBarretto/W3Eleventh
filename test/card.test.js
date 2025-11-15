const { expect } = require("chai")
const { ethers } = require("hardhat")

describe("CardStore (card tests)", () => {
    let Game, game, owner, player

    beforeEach(async () => {
        [owner, player] = await ethers.getSigners()
        Game = await ethers.getContractFactory("CardGame")
        game = await Game.deploy()
        await game.deployed()
    })

    it("rewards unique cards and stores attributes", async () => {
        const address = player.address

        const cardIdNumber = await cardIdFromTransaction(
            await game.awardUniqueCardTo(address, "Defender", 70)
        )
        const cardInfo = await game.cardDetails(cardIdNumber)

        expect(cardInfo[0]).to.equal("Defender")
        expect(cardInfo[1].toNumber()).to.equal(70)
        expect(cardInfo[2]).to.equal(address)

        const cardIdNumber2 = await cardIdFromTransaction(
            await game.awardUniqueCardTo(address, "Defender", 70)
        )

        expect(cardIdNumber).to.not.equal(cardIdNumber2)
        expect(await cardCount(game, address)).to.equal(2)
    })
})

const cardIdFromTransaction = async (tx1) => {
    return (await tx1.wait())
        .events
        .find((e) => e.event === 'CardWasAwarded')
        .args
        .cardId
        .toNumber()
}

const cardCount = async (cardGame, a) => {
    return (await cardGame.numberOfCardsInTeam(a)).toNumber()
}
