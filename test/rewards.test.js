const { expect } = require("chai")
const { ethers } = require("hardhat")

describe("Rewards (claim tests)", () => {
    let Game, game, host, guest

    beforeEach(async () => {
        [, host, guest] = await ethers.getSigners()
        Game = await ethers.getContractFactory("CardGame")
        game = await Game.deploy()
        await game.deployed()
    })

    it("allows winner to claim reward and mints a card", async () => {
        const hostsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(host.address, "Striker", 90)
        )
        
        const guestsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(guest.address, "Defender", 70)
        )
        
        await game.conductMatchBetween(hostsCard, guestsCard)
        expect(await rewardCount(game, host.address)).to.equal(1)

        const newId = await claimReward(game, host)
        expect(await cardCount(game, host.address)).to.be.greaterThan(1)
        expect(await rewardCount(game, host.address)).to.equal(0)

        const cardInfo = await game.cardDetails(newId)
        expect(cardInfo[2]).to.equal(host.address)
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

const claimReward = async (cardGame, player1) => {
    const claimTx = await cardGame.connect(player1).claimPendingReward()
    const rc = await claimTx.wait()
    const ev = rc.events.find((e) => e.event === 'RewardWasClaimed')
    const newId = ev.args.cardId.toNumber()
    return newId
}

const rewardCount = async (cardGame, a) => {
    return (await cardGame.pendingRewardCountFor(a)).toNumber()
}

const cardCount = async (cardGame, a) => {
    return (await cardGame.numberOfCardsInTeam(a)).toNumber()
}
