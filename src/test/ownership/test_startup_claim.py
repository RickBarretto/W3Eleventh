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


@scenario("Ownership.feature", "Gaining Claim rights for beginners")
def test_claim_at_startup():
    pass


@given("a player without any cards")
def player_without_cards(packages, players, ownership_ctx):
    player = players["alice"]
    ownership_ctx["player"] = player
    assert len(packages.cards_of(player)) == 0


@when("the player registers on the platform")
def register_player(packages, ownership_ctx):
    player = ownership_ctx["player"]
    with boa.env.prank(player):
        packages.register_player()


@then("the player is granted rights to claim a beginner card pack")
def beginner_claim_rights(packages, ownership_ctx):
    assert packages.claim_rights(ownership_ctx["player"])
