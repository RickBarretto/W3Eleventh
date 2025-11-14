import boa
import pytest
from pytest_bdd import *

from contracts.src import Admin


@pytest.fixture
def admins():
    return Admin.deploy()


@given("I am some User", target_fixture="some_user")
def some_user():
    return boa.env.generate_address()

@given("I am an Admin", target_fixture="admin")
def admin_user(admins, some_user):
    admins.add(some_user)
    assert admins.is_admin(some_user)
    return some_user

@given("I am not an Admin", target_fixture="non_admin")
def non_admin_user(admins, some_user):
    assert not admins.is_admin(some_user)
    return some_user



@scenario("Admin.feature", "Verifying Administrator")
def test_verify_admin():
    pass


@when("I try to verify if I am an Admin")
def verification():
    pass


@then("the verification should pass")
def should_be_admin(admins, admin):
    assert admins.is_admin(admin)

    

@scenario("Admin.feature", "Verifying non-Administrator User")
def test_verify_non_admin():
    pass


@when("I try to verify if I am an Admin")
def verification():
    pass


@then("the verification should fail")
def should_not_be_admin(admins, non_admin):
    assert not admins.is_admin(non_admin)
