import boa
import pytest
from pytest_bdd import *


@pytest.fixture
def ownership_ctx():
    return {}



@given("the blockchain is operational")
def ownership_blockchain_running():
    pass


@given("players have unique identifiers")
def ownership_unique_players(players):
    return players


@scenario("Ownership.feature", "Gaining Claim rights for winners")
def test_claim_for_winners():
    pass


@given("a player that has won a match")
def player_with_win_history(players, ownership_ctx):
    ownership_ctx["player"] = players["bob"]


@when("the player reaches a win milestone of 5 sequential wins")
def reach_win_milestone(packages_contract, admin, ownership_ctx):
    player = ownership_ctx["player"]
    for _ in range(5):
        with boa.env.prank(admin):
            packages_contract.record_win(player)


@then("the player is granted rights to claim a special card pack")
def special_claim_granted(packages_contract, ownership_ctx):
    assert packages_contract.claim_rights(ownership_ctx["player"])

