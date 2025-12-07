import boa
import pytest
from pytest_bdd import *

@pytest.fixture
def trade_ctx():
    return {}

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


@given("the blockchain is operational")
def trading_blockchain_running():
    pass


@given("players have unique identifiers")
def trading_unique_players(players):
    return players

@scenario("Trading.feature", "Trade Query")
def test_trade_after_victory():
    pass


@given("two players have traded cards")
def players_have_traded(packages_contract, admin, players, trade_ctx):
    winner_with_cards(packages_contract, admin, players, trade_ctx)
    propose_trade(packages_contract, trade_ctx)


@when("querying the blockchain for trade history")
def query_trade_history(packages_contract, trade_ctx):
    trade_ctx["trade_count"] = packages_contract.get_trade_count()
    trade_ctx["trade_details"] = packages_contract.get_trade(0)


@then("the response includes details of the trade")
def response_includes_trade(trade_ctx):
    assert trade_ctx["trade_count"] == 1
    assert len(trade_ctx["trade_details"]) == 4


@then("the involved players")
def response_includes_players(trade_ctx):
    from_addr, to_addr, _, _ = trade_ctx["trade_details"]
    assert {from_addr, to_addr} == {trade_ctx["winner"], trade_ctx["counterparty"]}


@then("the cards exchanged")
def response_includes_cards(trade_ctx):
    _, _, offered, requested = trade_ctx["trade_details"]
    assert {offered, requested} == {trade_ctx["offered_card"], trade_ctx["requested_card"]}
