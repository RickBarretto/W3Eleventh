const { expect } = require("chai")
const { ethers } = require("hardhat")

describe("CardGame (basic TDD tests)", () => {
    let Game, game, owner, host, guest

    beforeEach(async () => {
        [owner, host, guest] = await ethers.getSigners()

        Game = await ethers.getContractFactory("CardGame")
        game = await Game.deploy()

        await game.deployed()
    })

    it("creates a new team and is idempotent", async () => {
        const address = host.address
        await game.createNewTeamFor(address)
    
        expect(await hasTeam(game, address)).to.equal(true)
        expect(await cardCount(game, address)).to.equal(5)

        await game.createNewTeamFor(address)
        expect(await hasTeam(game, address)).to.equal(true)
        expect(await cardCount(game, address)).to.equal(5)
    })

    it("rewards unique cards and stores attributes", async () => {
        const address = guest.address
        const firstCardId = await cardIdFromTransaction(
            await game.awardUniqueCardTo(address, "Defender", 70)
        )
        const card = await game.cardDetails(firstCardId)
    
        expect(card[0]).to.equal("Defender")
        expect(card[1].toNumber()).to.equal(70)
        expect(card[2]).to.equal(address)

        const secondCardId = await cardIdFromTransaction(
            await game.awardUniqueCardTo(address, "Defender", 70)
        )
        const secondCard = await game.cardDetails(secondCardId)

        expect(secondCard[0]).to.equal("Defender")
        expect(secondCard[1].toNumber()).to.equal(70)
        expect(secondCard[2]).to.equal(address)

        expect(firstCardId).to.not.equal(secondCardId)
        expect(await cardCount(game, address)).to.equal(2)
    })

    it("determines match winners based on power and handles draws", async () => {
        const hostsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(host.address, "Striker", 90)
        )

        const guestsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(guest.address, "Defender", 70)
        )

        await game.conductMatchBetween(hostsCard, guestsCard)
        expect(await rewardCount(game, host.address)).to.equal(1)
        
        await claimReward(game, host)
        expect(await cardCount(game, host.address)).to.equal(2)

        const newHostsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(host.address, "Mid", 80)
        )

        const newGuestsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(guest.address, "Mid", 80)
        )

        const tx = await game.conductMatchBetween(newHostsCard, newGuestsCard)
        await tx.wait()

        expect(await rewardCount(game, host.address)).to.equal(0)
    })
})

const hasTeam = async (cardGame, hostAddress) => {
    return await cardGame.doesTeamExist(hostAddress)
}

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