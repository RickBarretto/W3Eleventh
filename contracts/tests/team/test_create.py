
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


@scenario("Team.feature", "Creating a Team")
def test_create_team():
	pass

@given('I want to create a new team named "Warriors"', target_fixture="team_name")
def team_name() -> TeamName:
	return "Warriors"

@when('I create the team "Warriors"')
def create_team(teams, team_name: TeamName):
	teams.new(team_name)

@then("I should own this team", target_fixture="found")
def team_should_exist(teams):
    team = teams.teams(boa.env.eoa)
    assert team
    return team

@then('its name should be "Warriors"')
def it_should_have_name(found):
	assert found.name == "Warriors"

@then("it should have 0 lost and won")
def it_should_have_no_matches(found):
	assert found.won == 0
	assert found.lost == 0