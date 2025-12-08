import boa
import pytest
from pytest_bdd import *


ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@pytest.fixture
def context():
    return {}


@scenario("Matches.feature", "Querying Match Details")
def test_finished():
    pass


@given("the blockchain is operational")
def blockchain_running():
    pass


@given("players have unique identifiers")
def unique_players(players):
    return players


@given("a match exists on the blockchain")
def match_exists(matches, players, context):
    host = players["alice"]
    guest = players["bob"]
    with boa.env.prank(host):
        match_id = matches.create_match()
    with boa.env.prank(guest):
        matches.join_match(match_id)
    # set squads and result to populate data
    with boa.env.prank(host):
        matches.choose_squad(match_id, b"host-squad")
    with boa.env.prank(guest):
        matches.choose_squad(match_id, b"guest-squad")
    with boa.env.prank(host):
        matches.report_result(match_id, host)
    context.update({"match_id": match_id, "host": host, "guest": guest})


@when("querying the blockchain for match details")
def query_match(matches, context):
    context["details"] = matches.get_match(context["match_id"])


@then("the response includes host, guest, status, squads, and winner")
def response_has_all_fields(context):
    host, guest, status, host_squad, guest_squad, winner = context["details"]
    assert host != ZERO_ADDRESS
    assert guest != ZERO_ADDRESS
    assert status in (1, 2)
    assert len(host_squad) > 0
    assert len(guest_squad) > 0
    assert winner in (host, guest)
