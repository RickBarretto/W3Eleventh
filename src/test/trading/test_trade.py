import boa
import pytest
from pytest_bdd import *


@pytest.fixture
def trading():
    return {}


@given("the blockchain is operational")
def trading_blockchain_running():
    pass


@given("players have unique identifiers")
def trading_unique_players(players):
    return players

@scenario("Trading.feature", "Trade after Match Victory")
def test_trade_after_victory():
    pass


@given("an ended match with a winner")
def winner_with_cards(packages, admin, players, trading):
    winner = players["alice"]
    counterparty = players["bob"]
    trading.update({"winner": winner, "counterparty": counterparty, "admin": admin})

    # Mint cards for both players to enable trading.
    with boa.env.prank(admin):
        packages.grant_claim(winner)
        packages.grant_claim(counterparty)
    with boa.env.prank(winner):
        packages.claim_pack()
    with boa.env.prank(counterparty):
        packages.claim_pack()

    trading["offered_card"] = packages.cards_of(winner)[0]
    trading["requested_card"] = packages.cards_of(counterparty)[0]


@when("the winner proposes a trade to another player")
def propose_trade(packages, trading):
    with boa.env.prank(trading["winner"]):
        packages.trade(
            trading["counterparty"],
            trading["offered_card"],
            trading["requested_card"],
        )
    trading["trade_executed"] = True


@then("the trade is done on the blockchain")
def trade_recorded(packages, trading):
    assert trading.get("trade_executed")
    assert packages.get_trade_count() == 1


@then("the offered card is transferred to the other player")
def offered_card_transferred(packages, trading):
    assert packages.card_owner(trading["offered_card"]) == trading["counterparty"]


@then("the requested card is transferred to the winner")
def requested_card_transferred(packages, trading):
    assert packages.card_owner(trading["requested_card"]) == trading["winner"]
