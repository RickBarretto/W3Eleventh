import boa
import pytest
from pytest_bdd import *

from contracts.src import Admin


@pytest.fixture
def admins():
    return Admin.deploy()


@given("I'm an Owner", target_fixture="owner")
def owner(admins):
    owner = boa.env.eoa
    assert admins.is_admin(owner)
    return owner

@given("I'm an Administrator", target_fixture="admin")
def admin(admins):
    address = boa.env.generate_address()
    admins.add(address)
    assert admins.is_admin(address)
    return address

@given("I'm a Customer", target_fixture="customer")
def customer(admins):
    address = boa.env.generate_address()
    assert not admins.is_admin(address)
    return address

@given("I have some address", target_fixture="some_address")
def some_address():
    return boa.env.generate_address()



@scenario("Admin.feature", "Registering a New Admin")
def test_register_admin():
    pass

@when("I register this new address as a new admin")
def register(admins, owner, some_address):
    admins.add(some_address)

@then("the new admin should be registered successfully")
def check_admin_registered(admins, some_address):
    assert admins.is_admin(some_address)



@scenario("Admin.feature", "No Permission to Register")
def test_register_admin_by_user():
    pass

@when("I try to register this new address as admin")
def register_attempt(admins, customer, some_address):
    with boa.env.prank(customer):
        with boa.reverts("Must be EOA"):
            admins.add(some_address)

@then('it should rollover "Must be EOA"')
def should_rollover(admins, some_address):
    assert not admins.is_admin(some_address)



@scenario("Admin.feature", "No Permission to Register (Admin)")
def test_register_admin_by_user_admin():
    pass

@when("I try to register this new address as admin (Admin)")
def register_attempt_admin(admins, admin, some_address):
    with boa.env.prank(admin):
        with boa.reverts("Must be EOA"):
            admins.add(some_address)

@then('it should rollover "Must be EOA" (Admin)')
def should_rollover(admins, some_address):
    assert not admins.is_admin(some_address)
