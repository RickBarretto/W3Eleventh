import boa
from boa.util.abi import Address
import pytest
from pytest_bdd import *

import contracts.src.Cards as Cards
import contracts.src.Inventory as Decks
import contracts.src.Trades as Trades


ZERO_ADDRESS = Address("0x0000000000000000000000000000000000000000")

cards = Cards()
decks = Decks(cards)
trades = Trades(decks)

@scenario("Trade.feature", "Accepted Trade")
def test_accepted_trade():
    pass

@given("a Trader A owning Card X", target_fixture="proposer")
def proposer():
    address = boa.env.generate_address()
    card = cards.new("Card X", 50)

    decks.mint_card_to(address, card)

    assert card in decks.deck_of(address)
    return address, card


@given("a Trader B owning Card Y", target_fixture="receiver")
def receiver():
    address = boa.env.generate_address()
    card = cards.new("Card Y", 75)

    decks.mint_card_to(address, card)

    assert card in decks.deck_of(address)
    return address, card


@when("Trader A proposes to trade Card X for Card Y to Trader B")
def on_proposal(proposer, receiver):
    proposer, given_card = proposer
    receiver, over_card = receiver

    with boa.env.prank(proposer):
        trades.propose(receiver, given_card.id, over_card.id)


@when("Trader B accepts the trade proposal")
def on_acceptance(proposer, receiver):
    proposer, _ = proposer
    receiver, _ = receiver

    print(decks.deck_of(proposer))
    print(decks.deck_of(receiver))

    with boa.env.prank(receiver):
        trades.accept(proposer)


@then("the Trade should happen")
def verify_trade_accepted(proposer, receiver):
    proposer, given_card = proposer
    receiver, over_card = receiver

    assert given_card in decks.deck_of(receiver)
    assert over_card in decks.deck_of(proposer)

    assert over_card not in decks.deck_of(receiver)
    assert given_card not in decks.deck_of(proposer)
