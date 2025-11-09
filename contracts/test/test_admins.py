import pytest
import boa

@pytest.fixture
def admins():
    return boa.load("contracts/src/Admins.vy")


def test_initial_admins(admins):
    assert admins.am_i()
    assert len(admins.all()) == 1


def test_am_i(admins):
    user = boa.env.generate_address()
    admins.include(user)

    with boa.env.prank(user):
        assert admins.am_i()


def test_include_admin(admins):
    user = boa.env.generate_address()
    admins.include(user)

    assert len(admins.all()) == 2
    assert admins.includes(user)


def test_exclude_admin(admins):
    user = boa.env.generate_address()
    admins.include(user)
    admins.exclude(user)

    assert len(admins.all()) == 1
    assert not admins.includes(user)