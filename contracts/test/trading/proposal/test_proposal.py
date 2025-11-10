import boa
from boa.util.abi import Address
import pytest
from pytest_bdd import *


ZERO_ADDRESS = Address("0x0000000000000000000000000000000000000000")

@pytest.fixture
def trades():
    return boa.load("contracts/src/Trades.vy")

@pytest.fixture
def cards():
    return boa.load("contracts/src/Cards.vy")

@pytest.fixture
def seller():
    return boa.env.generate_address()

@pytest.fixture
def buyer():
    return boa.env.generate_address()


@scenario("trading/Proposal.feature", "Sucessful Proposal")
def test_successful_proposal():
    pass


@given("a Card in auction", target_fixture="card_in_auction")
def card_in_auction(trades, cards, seller):
    card = cards.card("Card A", 100)

    with boa.env.prank(seller):
        trades.auction_card(card, 5)

    auction = trades.auction_of(seller)
    assert auction.seller == seller

    return card


@given("no proposals active by the Buyer", target_fixture="no_proposals_by_buyer")
def no_proposals_by_buyer(buyer, trades):
    with boa.env.prank(buyer):
        assert trades.empty_outbox()

@when("the Buyer proposes a trade", target_fixture="buyer_proposes_trade")
def buyer_proposes_trade(card_in_auction, no_proposals_by_buyer, trades, buyer, seller):
    with boa.env.prank(buyer):
        trades.propose(seller, card_in_auction)

    return buyer


@then("it should go the the proposal list")
def proposal_in_list(buyer_proposes_trade, trades, seller):
    with boa.env.prank(seller):
        assert len(trades.list_inbox()) == 1

