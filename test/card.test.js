const { ensure } = require('./helpers/ensure')
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

        ensure(cardInfo[0], "Defender")
        ensure(cardInfo[1].toNumber(), 70)
        ensure(cardInfo[2], address)

        const cardIdNumber2 = await cardIdFromTransaction(
            await game.awardUniqueCardTo(address, "Defender", 70)
        )

        ensure(() => cardIdNumber !== cardIdNumber2)
        ensure(await cardCount(game, address), 2)
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
