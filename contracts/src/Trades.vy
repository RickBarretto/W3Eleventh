# pragma version ^0.4.3
# pragma nonreentrancy on 

import Cards
import Inventory

initializes: Inventory
 
struct Proposal:
    by: address
    to: address
    given: uint256
    over: uint256

event TradeProposed:
    proposal: Proposal
    at: uint256

event TradeAccepted:
    proposal: Proposal
    at: uint256

event TradeRejected:
    proposal: Proposal
    at: uint256

proposals: HashMap[address, Proposal]


@deploy
def __init__():
    Inventory.__init__()


@external
def propose(_to: address, card_x: uint256, card_y: uint256):
    proposer: address = msg.sender
    receiver: address = _to

    assert Inventory.has_card(proposer, card_x), "Proposer does not own card_x"
    assert Inventory.has_card(receiver, card_y), "Other trader does not own card_y"

    proposal: Proposal = Proposal(by=proposer, to=receiver, given=card_x, over=card_y)
    self.proposals[proposer] = proposal

    log TradeProposed(proposal=proposal, at=block.timestamp)


@external
def accept(_proposer: address):
    proposer: address = _proposer
    receiver: address = msg.sender
    proposal: Proposal = self.proposals[proposer]

    assert proposal.to == receiver, "This proposal is not for the caller"
    assert Inventory.has_card(proposer, proposal.given), "Proposer no longer owns the offered card"
    assert Inventory.has_card(receiver, proposal.over), "Receiver no longer owns the requested card"

    given: Cards.Card = Inventory.card_of(proposer, proposal.given)
    over: Cards.Card = Inventory.card_of(receiver, proposal.over)
    given_idx: uint256 = Inventory.index_of(proposer, proposal.given)
    over_idx: uint256 = Inventory.index_of(receiver, proposal.over)

    Inventory.remove_from(proposer, given_idx)
    Inventory.remove_from(receiver, over_idx)

    Inventory.add_to(proposer, over)
    Inventory.add_to(receiver, given)

    self.proposals[proposer] = empty(Proposal)

    log TradeAccepted(proposal=proposal, at=block.timestamp)


@external
def reject(_proposer: address):
    proposer: address = _proposer
    receiver: address = msg.sender
    proposal: Proposal = self.proposals[proposer]

    assert proposal.to == receiver, "This proposal is not for the caller"
    self.proposals[proposer] = empty(Proposal)

    log TradeRejected(proposal=proposal, at=block.timestamp)