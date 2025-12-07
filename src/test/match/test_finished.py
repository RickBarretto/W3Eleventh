import boa
import pytest
from pytest_bdd import *


ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@pytest.fixture
def match_ctx():
    return {}


@scenario("Matches.feature", "Reporting Match Result")
def test_finished():
    pass


@given("the blockchain is operational")
def blockchain_running():
    pass


@given("players have unique identifiers")
def unique_players(players):
    return players

@given("a match in progress")
def match_in_progress(matches_contract, players, match_ctx):
    host = players["alice"]
    guest = players["bob"]
    with boa.env.prank(host):
        match_id = matches_contract.create_match()
    with boa.env.prank(guest):
        matches_contract.join_match(match_id)
    match_ctx.update({"match_id": match_id, "host": host, "guest": guest})


@given("one player has chosen its squad")
def one_squad_set(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    host = match_ctx["host"]

    with boa.env.prank(host):
        matches_contract.choose_squad(match_id, b"alice-ready")

    match_ctx["winner"] = host


@when("the second player chooses its squad")
def second_squad_and_result(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    host = match_ctx["host"]
    guest = match_ctx["guest"]

    guest_squad = b"bob-squad"
    with boa.env.prank(guest):
        matches_contract.choose_squad(match_id, guest_squad)

    match_ctx["winner"] = host
    with boa.env.prank(host):
        matches_contract.report_result(match_id, host)


@then("the match is updated on the blockchain")
def match_updated(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    _, _, status, *_ = matches_contract.matches(match_id)
    assert status in (1, 2)


@then("the winner is recorded")
def winner_recorded(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    *_, winner = matches_contract.matches(match_id)
    assert winner == match_ctx["winner"]


@then("the status is set to 2 (completed)")
def status_completed(matches_contract, match_ctx):
    match_id = match_ctx["match_id"]
    _, _, status, *_ = matches_contract.matches(match_id)
    assert status == 2
