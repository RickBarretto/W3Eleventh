const { expect } = require("chai")
const { ethers } = require("hardhat")

describe("MatchEngine (match tests)", () => {
    let Game, game, host, guest

    beforeEach(async () => {
        [, host, guest] = await ethers.getSigners()
        Game = await ethers.getContractFactory("CardGame")
        game = await Game.deploy()
        await game.deployed()
    })

    it("awards pending reward to winning card owner", async () => {
        const hostsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(host.address, "Striker", 90)
        )

        const guestsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(guest.address, "Defender", 70)
        )

        await game.conductMatchBetween(hostsCard, guestsCard)
        expect(await rewardCount(game, host.address)).to.equal(1)
        expect(await rewardCount(game, guest.address)).to.equal(0)
    })

    it("does not award pending reward on draw", async () => {
        const hostsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(host.address, "Mid", 80)
        )

        const guestsCard = await cardIdFromTransaction(
            await game.awardUniqueCardTo(guest.address, "Mid", 80)
        )

        await game.conductMatchBetween(hostsCard, guestsCard)
        expect(await rewardCount(game, host.address)).to.equal(0)
        expect(await rewardCount(game, guest.address)).to.equal(0)
    });
});

const cardIdFromTransaction = async (tx1) => {
    return (await tx1.wait())
        .events
        .find((e) => e.event === 'CardWasAwarded')
        .args
        .cardId
        .toNumber()
}

const rewardCount = async (cardGame, a) => {
    return (await cardGame.pendingRewardCountFor(a)).toNumber()
}
