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
shop: DynArray[Auction, 512]

# @dev Each user can expose only one card at a time
auctions: HashMap[address, Auction]

# @dev Each user can propose only one card at a time
proposals: HashMap[address, Proposal]


@external
def auction_of(_owner: address) -> Auction:
    return self.auctions[_owner]


@external
def auction_card(_card: Cards.Card, days: uint256) -> uint256:
    existing: Auction = self.auctions[msg.sender]

    is_owner: bool = existing.seller == msg.sender
    is_alive: bool = existing.end_at > block.timestamp
    is_active: bool = is_owner and is_alive

    assert not is_active, "You already have an active auction."

    auction: Auction = Auction(
        seller=msg.sender,
        card=_card,
        proposals=[],
        end_at=block.timestamp + days * ONE_DAY
    )

    self.shop.append(auction)
    self.auctions[msg.sender] = auction

    return len(self.shop) - 1

@external
def propose(to: address, card: Cards.Card) -> Proposal:
    proposal: Proposal = Proposal(
        proposer=msg.sender,
        offer=card
    )

    self.auctions[to].proposals.append(proposal)
    self.proposals[msg.sender] = proposal

    return proposal

@external
def list_outbox() -> Proposal:
    return self.proposals[msg.sender]

@external
def list_inbox() -> DynArray[Proposal, 64]:
    auction: Auction = self.auctions[msg.sender]
    return auction.proposals

@external
def empty_outbox() -> bool:
    proposal: Proposal = self.proposals[msg.sender]
    return proposal.proposer == empty(address)

@external
def empty_inbox() -> bool:
    auction: Auction = self.auctions[msg.sender]
    return len(auction.proposals) > 0
