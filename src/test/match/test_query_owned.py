import boa
import pytest
from pytest_bdd import *


ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@pytest.fixture
def context():
    return {}


@scenario("Matches.feature", "Querying Player Matches")
def test_finished():
    pass


@given("the blockchain is operational")
def blockchain_running():
    pass


@given("players have unique identifiers")
def unique_players(players):
    return players


@given("a player has participated in matches")
def player_with_history(matches_contract, players, context):
    player = players["alice"]
    other = players["bob"]
    third = players["carol"]

    # First match as host
    with boa.env.prank(player):
        first_id = matches_contract.create_match()
    with boa.env.prank(other):
        matches_contract.join_match(first_id)
    with boa.env.prank(player):
        matches_contract.choose_squad(first_id, b"alice-1")
    with boa.env.prank(other):
        matches_contract.choose_squad(first_id, b"bob-1")
    with boa.env.prank(player):
        matches_contract.report_result(first_id, player)

    # Second match as guest
    with boa.env.prank(third):
        second_id = matches_contract.create_match()
    with boa.env.prank(player):
        matches_contract.join_match(second_id)
    with boa.env.prank(third):
        matches_contract.choose_squad(second_id, b"carol-1")
    with boa.env.prank(player):
        matches_contract.choose_squad(second_id, b"alice-2")
    with boa.env.prank(player):
        matches_contract.report_result(second_id, player)

    context.update({"player": player, "history": [first_id, second_id]})


@when("querying the blockchain for matches involving the player")
def query_player_matches(matches_contract, context):
    context["player_matches"] = list(matches_contract.get_player_matches(context["player"]))


@then("the response includes all matches where the player is host or guest")
def all_matches_returned(context):
    returned = set(context["player_matches"])
    expected = set(context["history"])
    assert expected.issubset(returned)
