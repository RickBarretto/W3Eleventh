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
def player_with_history(matches, players, context):
    player = players["alice"]
    other = players["bob"]
    third = players["carol"]

    # First match as host
    with boa.env.prank(player):
        first_id = matches.create_match()
    with boa.env.prank(other):
        matches.join_match(first_id)
    with boa.env.prank(player):
        matches.choose_squad(first_id, b"alice-1")
    with boa.env.prank(other):
        matches.choose_squad(first_id, b"bob-1")
    with boa.env.prank(player):
        matches.report_result(first_id, player)

    # Second match as guest
    with boa.env.prank(third):
        second_id = matches.create_match()
    with boa.env.prank(player):
        matches.join_match(second_id)
    with boa.env.prank(third):
        matches.choose_squad(second_id, b"carol-1")
    with boa.env.prank(player):
        matches.choose_squad(second_id, b"alice-2")
    with boa.env.prank(player):
        matches.report_result(second_id, player)

    context.update({"player": player, "history": [first_id, second_id]})


@when("querying the blockchain for matches involving the player")
def query_player_matches(matches, context):
    context["player_matches"] = list(matches.get_player_matches(context["player"]))


@then("the response includes all matches where the player is host or guest")
def all_matches_returned(context):
    returned = set(context["player_matches"])
    expected = set(context["history"])
    assert expected.issubset(returned)
