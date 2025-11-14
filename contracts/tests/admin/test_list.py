import boa
import pytest
from pytest_bdd import *

from contracts.src import Admin


@pytest.fixture
def admins():
    return Admin.deploy()


@scenario("Admin.feature", "Listing All Admins")
def test_list_all_admins():
    pass


@given("I am an Admin")
def is_admin(admins):
    assert admins.is_admin(boa.env.eoa)
    boa.env.eoa


@given("there are multiple admins registered", target_fixture="expected_admins")
def have_multiples(admins):
    new_admin = boa.env.generate_address()
    admins.add(new_admin)
    
    assert admins.is_admin(boa.env.eoa)
    assert admins.is_admin(new_admin)

    return [boa.env.eoa, new_admin]


@when("I list all admins", target_fixture="actual_admins")
def list_admins(admins):
    return admins.all()


@then("I should see the list of all registered admins")
def check_admin_list(expected_admins, actual_admins):
    assert actual_admins == expected_admins
