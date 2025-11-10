from functools import partial
import boa
from boa.util.abi import Address
import pytest
from pytest_bdd import given, when, then, scenarios

# Register all scenarios from the feature file so step fixtures can be
# defined later in this module without ordering issues.
scenarios("../feature/trading/Auction.feature")

ZERO_ADDRESS = Address("0x0000000000000000000000000000000000000000")


@pytest.fixture
def trades():
    return boa.load("contracts/src/Trades.vy")

@pytest.fixture
def cards():
    return boa.load("contracts/src/Cards.vy")


# =========== Scenario 1 ===========


@given("a seller without any active auction", target_fixture="seller_without_active_auction")
def seller_without_active_auction(trades):
    seller = boa.env.generate_address()
    auction = trades.auction_of(seller)

    assert auction.seller == ZERO_ADDRESS
    return seller


@when("the seller auctions a card", target_fixture="auction_card")
def auction_card(seller_without_active_auction, trades, cards):
    owner = seller_without_active_auction
    card = cards.card("Card A", 99)

    with boa.env.prank(owner):
        trades.auction_card(card, 7)

    return owner


@then("the Auction should be registered.")
def auction_active_in_store(auction_card, trades):
    owner = auction_card
    auction = trades.auction_of(owner)

    assert auction.card.name == "Card A"
    assert auction.card.power == 99


# =========== Scenario 2 ===========


@given("a seller with an active auction", target_fixture="seller_with_active_auction")
def seller_with_active_auction(trades, cards):
    seller = boa.env.generate_address()
    card = cards.card("Card B", 50)

    with boa.env.prank(seller):
        trades.auction_card(card, 5)

    auction = trades.auction_of(seller)
    assert auction.seller == seller

    return seller


@when("the seller tries to auction another card", target_fixture="try_auction_another_card")
def try_auction_another_card(
    seller_with_active_auction,
    trades,
    cards,
):
    seller = seller_with_active_auction
    card = cards.card("Card C", 30)
    old_auction = trades.auction_of(seller)

    reverted = False
    with boa.env.prank(seller):
        try:
            trades.auction_card(card, 5)
        except Exception:
            reverted = True

    return seller, old_auction, reverted


@then("the Auction should be rejected")
def auction_rejected(try_auction_another_card, trades):
    seller, old_auction, reverted = try_auction_another_card
    
    assert reverted is True
    assert trades.auction_of(seller) == old_auction


@given("a seller with a dead auction", target_fixture="seller_with_dead_auction")
def seller_with_dead_auction(trades, cards):
    seller = boa.env.generate_address()
    card = cards.card("Card D", 20)
    with boa.env.prank(seller):
        trades.auction_card(card, 5)
    return seller


@when("the seller tries to auction another card (dead)", target_fixture="try_replace_dead_auction")
def try_replace_dead_auction():
    pass


@then("the new Auction should be registered")
def new_auction_registered(try_auction_another_card, trades):
    seller, old_auction, reverted = try_auction_another_card
    assert reverted is False
    assert trades.auction_of(seller) != old_auction
