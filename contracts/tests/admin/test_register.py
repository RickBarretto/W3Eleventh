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

@given("I have a Candidate", target_fixture="candidate")
def candidate():
    return boa.env.generate_address()



@scenario("Admin.feature", "Successfully Registering a New Admin")
def test_successful_registering():
    pass

@when("I register this new address as a new admin")
def try_register(admins, owner, candidate):
    admins.add(candidate)

@then("the new admin should be registered successfully")
def should_be_registered(admins, candidate):
    assert admins.is_admin(candidate)



@scenario("Admin.feature", "Customer Trying to Register New Admin")
def test_customer_trying_to_register_new_admin():
    pass

@when("I try to register this new address as admin")
def try_register(admins, customer, candidate):
    pass

@then('it should rollover "Must be EOA"')
def should_rollover(admins, customer, candidate):
    with boa.env.prank(customer):
        with boa.reverts("Must be EOA"):
            admins.add(candidate)

    assert not admins.is_admin(candidate)


@scenario("Admin.feature", "Admin Trying to Register New Admin")
def test_admin_trying_to_register_new_admin():
    pass

@when("I try to register this new address as admin (Admin)")
def try_to_register():
    pass

@then('it should rollover "Must be EOA" (Admin)')
def should_rollover(admins, admin, candidate):
    with boa.env.prank(admin):
        with boa.reverts("Must be EOA"):
            admins.add(candidate)

    assert not admins.is_admin(candidate)