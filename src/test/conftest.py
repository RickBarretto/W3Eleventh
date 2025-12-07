"""Utils used across tests."""

from pathlib import Path

import boa
import pytest

from src.smart import Matches
from src.smart import Packages

ROOT_DIR = Path(__file__).resolve().parents[2]
CONTRACTS_DIR = ROOT_DIR / "src" / "smart"


new_address = boa.env.generate_address


@pytest.fixture(autouse=True)
def boa_env():
    """Reset the environment after each test."""
    with boa.env.anchor():
        yield


@pytest.fixture
def admin():
    """Admin's address"""
    return new_address("admin")


@pytest.fixture
def players():
    """Group of player addresses"""
    return {
        "alice": new_address("alice"),
        "bob": new_address("bob"),
        "carol": new_address("carol"),
        "dave": new_address("dave"),
    }


@pytest.fixture
def matches():
    """Match contract instance"""
    return Matches()


@pytest.fixture
def packages(admin):
    """Packages contract instance"""
    with boa.env.prank(admin):
        return Packages(admin)
