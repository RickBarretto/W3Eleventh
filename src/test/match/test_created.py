import boa
import pytest
from pytest_bdd import *


ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@pytest.fixture
def match_ctx():
    return {}


@scenario("Matches.feature", "Creating a Match")
def test_created():
    pass


@given("the blockchain is operational")
def blockchain_running():
    pass


@given("players have unique identifiers")
def unique_players(players):
    return players


@given("one player is ready to play")
def host_ready(players, match_ctx):
    match_ctx["host"] = players["alice"]



@when("a match is initiated")
def create_match(matches_contract, match_ctx):
    host = match_ctx["host"]
    with boa.env.prank(host):
        match_ctx["match_id"] = matches_contract.create_match()

@then("the match is recorded on the blockchain")
def match_recorded(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    host, _, status, _, _, _ = matches_contract.matches(match_id)
    assert host != ZERO_ADDRESS
    assert status == 0


@then("the host is registered as the match host")
def host_is_registered(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    host = match_ctx["host"]
    stored_host, _, _, _, _, _ = matches_contract.matches(match_id)
    assert stored_host == host


@then("the status is set to 0 (waiting)")
def status_waiting(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    _, _, status, _, _, _ = matches_contract.matches(match_id)
    assert status == 0


@then("there is no guest yet")
def no_guest(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    _, guest, _, _, _, _ = matches_contract.matches(match_id)
    assert guest == ZERO_ADDRESS


@then("there is no winner yet")
def no_winner(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    _, _, _, _, _, winner = matches_contract.matches(match_id)
    assert winner == ZERO_ADDRESS


