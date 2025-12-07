import boa
import pytest
from pytest_bdd import *


@pytest.fixture
def trade_ctx():
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
def winner_with_cards(packages_contract, admin, players, trade_ctx):
    winner = players["alice"]
    counterparty = players["bob"]
    trade_ctx.update({"winner": winner, "counterparty": counterparty, "admin": admin})

    # Mint cards for both players to enable trading.
    with boa.env.prank(admin):
        packages_contract.grant_claim(winner)
        packages_contract.grant_claim(counterparty)
    with boa.env.prank(winner):
        packages_contract.claim_pack()
    with boa.env.prank(counterparty):
        packages_contract.claim_pack()

    trade_ctx["offered_card"] = packages_contract.cards_of(winner)[0]
    trade_ctx["requested_card"] = packages_contract.cards_of(counterparty)[0]


@when("the winner proposes a trade to another player")
def propose_trade(packages_contract, trade_ctx):
    with boa.env.prank(trade_ctx["winner"]):
        packages_contract.trade(
            trade_ctx["counterparty"],
            trade_ctx["offered_card"],
            trade_ctx["requested_card"],
        )
    trade_ctx["trade_executed"] = True


@then("the trade is done on the blockchain")
def trade_recorded(packages_contract, trade_ctx):
    assert trade_ctx.get("trade_executed")
    assert packages_contract.get_trade_count() == 1


@then("the offered card is transferred to the other player")
def offered_card_transferred(packages_contract, trade_ctx):
    assert packages_contract.card_owner(trade_ctx["offered_card"]) == trade_ctx["counterparty"]


@then("the requested card is transferred to the winner")
def requested_card_transferred(packages_contract, trade_ctx):
    assert packages_contract.card_owner(trade_ctx["requested_card"]) == trade_ctx["winner"]
