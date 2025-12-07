import boa
import pytest
from pytest_bdd import *


ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@pytest.fixture
def match_ctx():
    return {}


@scenario("Matches.feature", "Joining a Match")
def test_joined():
    pass


@given("the blockchain is operational")
def blockchain_running():
    pass


@given("players have unique identifiers")
def unique_players(players):
    return players


@given("a waiting match")
def waiting_match(matches_contract, players, match_ctx):
    host = players["alice"]
    with boa.env.prank(host):
        match_ctx["match_id"] = matches_contract.create_match()
    match_ctx["host"] = host


@when("another player joins the match")
def join_waiting_match(matches_contract, players, match_ctx):
    match_id = match_ctx["match_id"]
    guest = players["bob"]
    match_ctx["guest"] = guest
    with boa.env.prank(guest):
        matches_contract.join_match(match_id)


@then("the match is updated on the blockchain")
def match_updated(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    _, _, status, *_ = matches_contract.matches(match_id)
    assert status in (1, 2)


@then("the guest is registered as the guest player")
def guest_registered(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    _, guest, *_ = matches_contract.matches(match_id)
    assert guest == match_ctx["guest"]


@then("the status is set to 1 (in progress)")
def status_in_progress(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    _, _, status, *_ = matches_contract.matches(match_id)
    assert status == 1
