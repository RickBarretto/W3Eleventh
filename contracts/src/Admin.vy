
owner: public(address)
admin: public(DynArray[address, 128])


@deploy
def __init__():
    self.owner = msg.sender
    self.admin.append(msg.sender)


@external
def add(new_admin: address):
    """Register a new admin address. Only callable by the owner."""
    assert msg.sender == self.owner, "Must be EOA"
    assert new_admin not in self.admin, "Already admin"
    self.admin.append(new_admin)


@view
@external
def all() -> DynArray[address, 128]:
    """Get the list of all admin addresses."""
    assert self._is_admin(msg.sender), "Must be Admin"
    return self.admin


@view
@external
def is_admin(check_address: address) -> bool:
    """Check if an address is an admin."""
    return self._is_admin(check_address)

@view
def _is_admin(check_address: address) -> bool:
    """Internal function to check if an address is an admin."""
    return check_address in self.admin
