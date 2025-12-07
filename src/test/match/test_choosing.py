import boa
import pytest
from pytest_bdd import *


ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@pytest.fixture
def context():
    return {}


@scenario("Matches.feature", "Choosing a Squad")
def test_choosing():
    pass


@given("the blockchain is operational")
def blockchain_running():
    pass


@given("players have unique identifiers")
def unique_players(players):
    return players

@given("a match is in progress")
def match_in_progress(matches_contract, players, context):
    host = players["alice"]
    guest = players["bob"]
    with boa.env.prank(host):
        match_id = matches_contract.create_match()
    with boa.env.prank(guest):
        matches_contract.join_match(match_id)
    context.update({"match_id": match_id, "host": host, "guest": guest})


@given("both players are registered")
def players_registered(context):
    assert "host" in context and "guest" in context


@given("have not chosen their squads yet")
def squads_empty(matches_contract, context):
    match_id = context["match_id"]
    _, _, _, host_squad, guest_squad, _ = matches_contract.matches(match_id)
    assert len(host_squad) == 0
    assert len(guest_squad) == 0


@when("a player chooses a squad")
def choose_squad(matches_contract, context):
    match_id = context["match_id"]
    host = context["host"]
    squad = b"alice-squad"
    with boa.env.prank(host):
        matches_contract.choose_squad(match_id, squad)
    context["chosen_player"] = host
    context["chosen_squad"] = squad


@then("the match is updated on the blockchain")
def match_updated(matches_contract, context):
    match_id = context["match_id"]
    _, _, status, _, _, _ = matches_contract.matches(match_id)
    assert status in (1, 2)


@then("the player's chosen squad is recorded")
def squad_recorded(matches_contract, context):
    match_id = context["match_id"]
    stored = matches_contract.matches(match_id)
    stored_host_squad = stored[3]
    assert stored_host_squad == context["chosen_squad"]
