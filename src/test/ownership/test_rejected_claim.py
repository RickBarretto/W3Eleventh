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


@scenario("Ownership.feature", "Rejected Claim")
def test_rejected_claim():
    pass



@given("a player without claiming rights")
def player_no_claim(players, ownership_ctx, packages_contract):
    player = players["carol"]
    ownership_ctx["player"] = player
    assert not packages_contract.claim_rights(player)


@when("the player tries to claim a card pack")
def attempt_claim_without_rights(packages_contract, ownership_ctx):
    player = ownership_ctx["player"]
    with boa.env.prank(player):
        with boa.reverts("no claim rights"):
            packages_contract.claim_pack()
    ownership_ctx["claim_failed"] = True


@then("the blockchain rejects the request")
def blockchain_rejects(ownership_ctx):
    assert ownership_ctx.get("claim_failed"), "Expected request rejection flag not set"


@then("an error message is returned indicating the player cannot claim a card pack")
def claim_error_message():
    # boa.reverts asserted the revert reason
    pass
