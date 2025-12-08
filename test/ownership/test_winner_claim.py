import boa
import pytest
from pytest_bdd import *


@pytest.fixture
def context():
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
def player_with_win_history(players, context):
    context["player"] = players["bob"]


@when("the player reaches a win milestone of 5 sequential wins")
def reach_win_milestone(packages, admin, context):
    player = context["player"]
    for _ in range(5):
        with boa.env.prank(admin):
            packages.record_win(player)


@then("the player is granted rights to claim a special card pack")
def special_claim_granted(packages, context):
    assert packages.claim_rights(context["player"])

