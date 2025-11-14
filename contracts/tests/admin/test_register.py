import boa
import pytest
from pytest_bdd import *

from contracts.src import Admin


@pytest.fixture
def admins():
    return Admin.deploy()


@given("I am an Externally Owned Admin", target_fixture="eoa")
def admin(admins):
    eoa = boa.env.eoa
    assert admins.is_admin(eoa)
    return eoa

@given("I am not an Admin", target_fixture="non_admin")
def non_admin(admins):
    some_address = boa.env.generate_address()
    assert not admins.is_admin(some_address)
    return some_address

@given("I have some address", target_fixture="some_address")
def some_address():
    return boa.env.generate_address()



@scenario("Admin.feature", "Registering a New Admin")
def test_register_admin():
    pass

@when("I register this new address as a new admin")
def register(admins, eoa, some_address):
    with boa.env.prank(eoa):
        admins.add(some_address)

@then("the new admin should be registered successfully")
def check_admin_registered(admins, some_address):
    assert admins.is_admin(some_address)



@scenario("Admin.feature", "No Permission to Register")
def test_register_admin_by_user():
    pass

@when("I try to register this new address as admin")
def register_attempt(admins, non_admin, some_address):
    with boa.reverts("Must be admin"):
        admins.add(some_address, sender=non_admin)

@then('it should rollover "Insufficient permission"')
def should_rollover(admins, some_address):
    assert not admins.is_admin(some_address)
