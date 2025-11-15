const { expect } = require("chai")
const { ethers } = require("hardhat")

describe("CardGame (basic TDD tests)", function () {
    let CardGame, cardGame, owner, host, guest

    beforeEach(async function () {
        [owner, host, guest] = await ethers.getSigners()

        CardGame = await ethers.getContractFactory("CardGame")
        cardGame = await CardGame.deploy()

        await cardGame.deployed()
    })

    it("creates a new team and is idempotent", async function () {
        const hostAddress = host.address
        await cardGame.createNewTeamFor(hostAddress)
    
        expect(await hasTeam(cardGame, hostAddress)).to.equal(true)
        expect(await cardCount(cardGame, hostAddress)).to.equal(5)

        await cardGame.createNewTeamFor(hostAddress)
        expect(await hasTeam(cardGame, hostAddress)).to.equal(true)
        expect(await cardCount(cardGame, hostAddress)).to.equal(5)
    })

    it("rewards unique cards and stores attributes", async function () {
        const guestAddress = guest.address
        const guestsCardId = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(guestAddress, "Defender", 70)
        )
        const guestCard = await cardGame.cardDetails(guestsCardId)
    
        expect(guestCard[0]).to.equal("Defender")
        expect(guestCard[1].toNumber()).to.equal(70)
        expect(guestCard[2]).to.equal(guestAddress)

        const guestsCardId2 = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(guestAddress, "Defender", 70)
        )
        const guestCard2 = await cardGame.cardDetails(guestsCardId2)

        expect(guestCard2[0]).to.equal("Defender")
        expect(guestCard2[1].toNumber()).to.equal(70)
        expect(guestCard2[2]).to.equal(guestAddress)

        expect(guestsCardId).to.not.equal(guestsCardId2)
        expect(await cardCount(cardGame, guestAddress)).to.equal(2)
    })

    it("determines match winners based on power and handles draws", async function () {
        const hostAddress = host.address
        const guestAddress = guest.address

        const hostsCard = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(hostAddress, "Striker", 90)
        )

        const guestsCard = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(guestAddress, "Defender", 70)
        )

        await cardGame.conductMatchBetween(hostsCard, guestsCard)
        expect((await cardGame.pendingRewardCountFor(hostAddress)).toNumber()).to.equal(1)

        const _ = await claimReward(cardGame, host)
        expect( await cardCount(cardGame, hostAddress)).to.equal(2)

        const newHostsCard = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(hostAddress, "Mid", 80)
        )

        const newGuestsCard = await cardIdFromTransaction(
            await cardGame.awardUniqueCardTo(guestAddress, "Mid", 80)
        )

        const tx = await cardGame.conductMatchBetween(newHostsCard, newGuestsCard)
        await tx.wait()
        expect((await cardGame.pendingRewardCountFor(hostAddress)).toNumber()).to.equal(0)
    })
})

async function hasTeam(cardGame, hostAddress) {
    return await cardGame.doesTeamExist(hostAddress)
}

async function cardIdFromTransaction(tx1) {
    return (await tx1.wait())
        .events
        .find((e) => e.event === 'CardWasAwarded')
        .args
        .cardId
        .toNumber()
}

async function claimReward(cardGame, player1) {
    const claimTx = await cardGame.connect(player1).claimPendingReward()
    const rc = await claimTx.wait()
    const ev = rc.events.find((e) => e.event === 'RewardWasClaimed')
    const newId = ev.args.cardId.toNumber()
    return newId
}

async function rewardCount(cardGame, a) {
    return (await cardGame.pendingRewardCountFor(a)).toNumber()
}

async function cardCount(cardGame, a) {
    return (await cardGame.numberOfCardsInTeam(a)).toNumber()
}