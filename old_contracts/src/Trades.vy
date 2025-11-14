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
def __init__(decks: address):
    Inventory = decks


@external
def propose(_to: address, card_x: uint256, card_y: uint256):
    proposer: address = msg.sender
    receiver: address = _to

    proposal: Proposal = Proposal(by=proposer, to=receiver, given=card_x, over=card_y)
    self.proposals[proposer] = proposal

    log TradeProposed(proposal=proposal, at=block.timestamp)


@external
def accept(_proposer: address):
    proposer: address = _proposer
    receiver: address = msg.sender
    proposal: Proposal = self.proposals[proposer]

    assert proposer != empty(address), "Proposer address cannot be zero"
    assert receiver != empty(address), "Receiver address cannot be zero"
    assert proposal.to == receiver, "This proposal is not for the caller"
    
    given: Cards.Card = empty(Cards.Card)
    over: Cards.Card = empty(Cards.Card)

    proposer_deck: DynArray[Cards.Card, 64] = Inventory._deck_of(proposer)
    for card: Cards.Card in proposer_deck:
        if card.id == proposal.given:
            given = card
            break

    receiver_deck: DynArray[Cards.Card, 64] = Inventory._deck_of(receiver)
    for card: Cards.Card in receiver_deck:
        if card.id == proposal.over:
            over = card
            break

    Inventory.set_card(receiver, over, given)
    Inventory.set_card(proposer, given, over)

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