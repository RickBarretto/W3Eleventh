
import boa
from boa.util.abi import Address
import pytest
from pytest_bdd import *

from contracts.src import Teams


type Owner = Address
type Player = Address
type TeamName = str


@pytest.fixture
def teams():
	return Teams.deploy()


@scenario("Team.feature", "Winning a match")
def test_won():
	pass

@given('a Team "Warriors" with 0 won')
def team_name(teams):
	teams.new("Warriors")

@when("it wins a match")
def have_won(teams):
	teams.win(boa.env.eoa)

@then("it has 1 won")
def team_should_exist(teams):
    team = teams.teams(boa.env.eoa)
    assert team.won == 1
    assert team.lost == 0


@scenario("Team.feature", "Winning a match")
def test_lost():
	pass

@given('a Team "Warriors" with 0 lost')
def team_name(teams):
	teams.new("Warriors")

@when("it loses a match")
def have_won(teams):
	teams.lose(boa.env.eoa)

@then("it has 1 lost")
def team_should_exist(teams):
    team = teams.teams(boa.env.eoa)
    assert team.won == 0
    assert team.lost == 1
