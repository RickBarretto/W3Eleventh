import boa
from boa.util.abi import Address
import pytest
from pytest_bdd import *

from contracts.src import Admin


type Administrator = Address
type Customer = Address

@pytest.fixture
def admins():
    return Admin.deploy()


@given("I am an Administrator")
def is_admin(admins):
    assert admins.is_admin(boa.env.eoa)
    boa.env.eoa
    
@given("I am not an Administrator", target_fixture="customer")
def customer(admins) -> Customer:
    address: Address = boa.env.generate_address()
    assert not admins.is_admin(address)
    return address

@given("there are multiple administrators registered", target_fixture="expected_admins")
def have_multiples(admins) -> list[Administrator]:
    new_admin = boa.env.generate_address()
    admins.add(new_admin)
    
    assert admins.is_admin(boa.env.eoa)
    assert admins.is_admin(new_admin)

    return [boa.env.eoa, new_admin]



@scenario("Admin.feature", "Listing All Admins")
def test_list_all_admins():
    pass

@when("I try to list all administrators¹", target_fixture="actual_admins")
def list_admins(admins) -> list[Administrator]:
    return admins.all()

@then("I should see the list of all registered administrators")
def check_admin_list(expected_admins: list[Administrator], actual_admins: list[Administrator]):
    assert actual_admins == expected_admins



@scenario("Admin.feature", "No Permission to Listing")
def test_cannot_list():
    pass

@when("I try to list all administrators²")
def try_list():
    pass

@then('it should rollover "Must be Admin"')
def should_fail(admins, customer: Customer):
    with boa.env.prank(customer):
        with boa.reverts("Must be Admin"):
            admins.all()
