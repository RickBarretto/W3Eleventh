import boa
import pytest
from pytest_bdd import *

from contracts.src import Admin


@pytest.fixture
def admins():
    return Admin.deploy()


@scenario("Admin.feature", "Registering a New Admin")
def test_register_admin():
    pass


@given("I am an Admin")
def admin(admins):
    assert admins.is_admin(boa.env.eoa)

@given("I have some address", target_fixture="some_address")
def some_address():
    return boa.env.generate_address()


@when("I register this new address as a new admin")
def register(admins, some_address):
    admins.add(some_address)


@then("the new admin should be registered successfully")
def check_admin_registered(admins, some_address):
    assert admins.is_admin(some_address)
