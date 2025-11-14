import boa
from boa.util.abi import Address
import pytest
from pytest_bdd import *

from contracts.src import Admin as Admins


type Owner = Address
type Administrator = Address
type Customer = Address
type Candidate = Address


@pytest.fixture
def admins():
    return Admins.deploy()


@given("I'm an Owner", target_fixture="owner")
def owner(admins) -> Owner:
    owner: Address = boa.env.eoa
    assert admins.is_admin(owner)
    return owner

@given("I'm an Administrator", target_fixture="admin")
def admin(admins) -> Administrator:
    address: Address = boa.env.generate_address()
    admins.add(address)
    assert admins.is_admin(address)
    return address

@given("I'm a Customer", target_fixture="customer")
def customer(admins) -> Customer:
    address: Address = boa.env.generate_address()
    assert not admins.is_admin(address)
    return address

@given("I have a Candidate", target_fixture="candidate")
def candidate() -> Candidate:
    return boa.env.generate_address()



@scenario("Admin.feature", "Successfully Registering a New Admin")
def test_by_owner():
    pass

@when("I try to register Candidate as a new admin¹")
def try_register(admins, candidate: Candidate):
    admins.add(candidate)

@then("the new admin should be registered successfully")
def should_be_registered(admins, candidate: Candidate):
    assert admins.is_admin(candidate)



@scenario("Admin.feature", "Customer Trying to Register New Admin")
def test_by_customer():
    pass

@when("I try to register Candidate as a new admin²")
def try_register():
    pass

@then('it should rollover "Must be EOA"¹')
def should_rollover(admins, customer: Customer, candidate: Candidate):
    with boa.env.prank(customer):
        with boa.reverts("Must be EOA"):
            admins.add(candidate)

    assert not admins.is_admin(candidate)


@scenario("Admin.feature", "Admin Trying to Register New Admin")
def test_by_admin():
    pass

@when("I try to register Candidate as a new admin³")
def try_register():
    pass

@then('it should rollover "Must be EOA"²')
def should_rollover(admins, admin: Administrator, candidate: Candidate):
    with boa.env.prank(admin):
        with boa.reverts("Must be EOA"):
            admins.add(candidate)

    assert not admins.is_admin(candidate)