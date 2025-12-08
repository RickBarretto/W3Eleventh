import boa
import pytest
from pytest_bdd import *


ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@pytest.fixture
def context():
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
def waiting_match(matches, players, context):
    host = players["alice"]
    with boa.env.prank(host):
        context["match_id"] = matches.create_match()
    context["host"] = host


@when("another player joins the match")
def join_waiting_match(matches, players, context):
    match_id = context["match_id"]
    guest = players["bob"]
    context["guest"] = guest
    with boa.env.prank(guest):
        matches.join_match(match_id)


@then("the match is updated on the blockchain")
def match_updated(matches, context):
    match_id = context["match_id"]
    _, _, status, *_ = matches.matches(match_id)
    assert status in (1, 2)


@then("the guest is registered as the guest player")
def guest_registered(matches, context):
    match_id = context["match_id"]
    _, guest, *_ = matches.matches(match_id)
    assert guest == context["guest"]


@then("the status is set to 1 (in progress)")
def status_in_progress(matches, context):
    match_id = context["match_id"]
    _, _, status, *_ = matches.matches(match_id)
    assert status == 1
