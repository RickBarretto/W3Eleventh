from pathlib import Path

import boa
import pytest

ROOT_DIR = Path(__file__).resolve().parents[2]
CONTRACTS_DIR = ROOT_DIR / "src" / "smart"


@pytest.fixture(autouse=True)
def boa_env():
    # Anchor the environment so state changes are reverted after each test.
    with boa.env.anchor():
        yield


@pytest.fixture
def admin():
    return boa.env.generate_address("admin")


@pytest.fixture
def players():
    return {
        "alice": boa.env.generate_address("alice"),
        "bob": boa.env.generate_address("bob"),
        "carol": boa.env.generate_address("carol"),
        "dave": boa.env.generate_address("dave"),
    }


@pytest.fixture
def matches_contract():
    return boa.load(str(CONTRACTS_DIR / "Matches.vy"))


@pytest.fixture
def packages_contract(admin):
    with boa.env.prank(admin):
        return boa.load(str(CONTRACTS_DIR / "Packages.vy"), admin)
