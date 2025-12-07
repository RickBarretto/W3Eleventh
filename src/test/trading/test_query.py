import boa
import pytest
from pytest_bdd import *

@pytest.fixture
def trading():
    return {}

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
def players_have_traded(packages, admin, players, trading):
    winner_with_cards(packages, admin, players, trading)
    propose_trade(packages, trading)


@when("querying the blockchain for trade history")
def query_trade_history(packages, trading):
    trading["trade_count"] = packages.get_trade_count()
    trading["trade_details"] = packages.get_trade(0)


@then("the response includes details of the trade")
def response_includes_trade(trading):
    assert trading["trade_count"] == 1
    assert len(trading["trade_details"]) == 4


@then("the involved players")
def response_includes_players(trading):
    from_addr, to_addr, _, _ = trading["trade_details"]
    assert {from_addr, to_addr} == {trading["winner"], trading["counterparty"]}


@then("the cards exchanged")
def response_includes_cards(trading):
    _, _, offered, requested = trading["trade_details"]
    assert {offered, requested} == {trading["offered_card"], trading["requested_card"]}
