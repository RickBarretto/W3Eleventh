#pragma version ^0.4.3
# pragma nonreentrancy on 

import Cards


struct Proposal:
    proposer: address
    offer: Cards.Card

struct Auction:
    seller: address
    card: Cards.Card
    proposals: DynArray[Proposal, 64]
    end_at: uint256


ONE_MINUTE: constant(uint256) = 60
ONE_HOUR: constant(uint256) = 60 * ONE_MINUTE
ONE_DAY: constant(uint256) = 24 * ONE_HOUR
ONE_WEEK: constant(uint256) = 7 * ONE_DAY

# @dev Each auction listed in the marketplace
shop: public(DynArray[Auction, 512])

# @dev Each user can expose only one card at a time
auctions: public(HashMap[address, Auction]) 

# @dev Each user can propose only one card at a time
proposals: public(HashMap[address, Proposal])


@deploy
def __init__():
    pass

@external
def my_auctions() -> Auction:
    return self.auctions[msg.sender]

@external
def my_proposals() -> Proposal:
    return self.proposals[msg.sender]

@external
def auction_card(card: Cards.Card, days: uint256):
    assert days > 0, "Auction duration must be at least one day."
    assert self.auctions[msg.sender].seller == empty(address), "You already have an active auction."

    auction: Auction = Auction(
        seller=msg.sender,
        card=card,
        proposals=empty(DynArray[Proposal, 64]),
        end_at=block.timestamp + days * ONE_DAY
    )

    self.shop.append(auction)
    self.auctions[msg.sender] = auction

@external
def propose(auction_index: uint256, card: Cards.Card):
    auction: Auction = self.shop[auction_index]

    assert block.timestamp < auction.end_at, "Auction has ended"
    assert auction.seller != msg.sender, "Cannot propose on your own auction."
    assert self.proposals[msg.sender].proposer == empty(address), "You have already proposed."

    proposal: Proposal = Proposal(
        proposer=msg.sender,
        offer=card,
    )

    auction.proposals.append(proposal)
    self.proposals[msg.sender] = proposal
