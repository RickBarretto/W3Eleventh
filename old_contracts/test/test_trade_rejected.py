import boa
from boa.util.abi import Address
import pytest
from pytest_bdd import *


ZERO_ADDRESS = Address("0x0000000000000000000000000000000000000000")

@pytest.fixture
def trades():
    return boa.load("contracts/src/Trades.vy")

@pytest.fixture
def decks():
    return boa.load("contracts/src/Inventory.vy")

@pytest.fixture
def cards():
    return boa.load("contracts/src/Cards.vy")


@scenario("Trade.feature", "Rejected Trade")
def test_rejected_trade():
    pass

@given("a Trader A owning Card X", target_fixture="trader_a")
def trader_a(cards, decks, trades):
    trader_a = boa.env.generate_address()
    card_x = cards.new("Card X", 50)

    decks.mint_card_to(trader_a, card_x)

    assert card_x in decks.deck_of(trader_a)
    
    return trader_a, card_x


@given("a Trader B owning Card Y", target_fixture="trader_b")
def trader_b(cards, decks, trades):
    trader_b = boa.env.generate_address()
    card_y = cards.new("Card Y", 75)

    decks.mint_card_to(trader_b, card_y)

    assert card_y in decks.deck_of(trader_b)

    return trader_b, card_y


@when("Trader A proposes to trade Card X for Card Y to Trader B")
def on_proposal(trader_a, trader_b, decks, trades):
    trader_a, card_x = trader_a
    trader_b, card_y = trader_b

    with boa.env.prank(trader_a):
        trades.propose(trader_b, card_x, card_y)

    return trader_a, trader_b, card_x, card_y


@when("Trader B rejects the trade proposal")
def on_rejection(on_proposal, trades):
    trader_a, trader_b, card_x, card_y = on_proposal

    with boa.env.prank(trader_b):
        trades.reject(trader_a, card_x, card_y)


@then("the Trade should not happen")
def verify_trade_rejected(trader_a, trader_b, on_rejection, decks):
    trader_a, card_x = trader_a
    trader_b, card_y = trader_b

    assert card_x in decks.deck_of(trader_a)
    assert card_x not in decks.deck_of(trader_b)

    assert card_y in decks.deck_of(trader_b)
    assert card_y not in decks.deck_of(trader_a)
