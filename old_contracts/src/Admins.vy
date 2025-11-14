# pragma version ^0.4.3
# pragma nonreentrancy on 

main_admin: address
admins: DynArray[address, 256]


@deploy
def __init__():
    self.main_admin = msg.sender


# Decorator function
def must_be(_user: address):
    """Decorator to restrict function access to admins only.

    Usage
    -----
        @external
        def admin_function():
            Admins.must_be()

    Future
    ------
    This function could be used as a decorator for other functions to enforce admin-only access.
    But Vyper currently does not support decorators directly.

        @admin
        @external
        def some_function():
            ... 
    """
    assert self.is_admin(_user), "Only admins can perform this action."


@external
def all() -> DynArray[address, 257]:
    self.must_be(msg.sender)

    buffer: DynArray[address, 257] = empty(DynArray[address, 257])

    buffer.append(self.main_admin)
    for admin: address in self.admins:
        buffer.append(admin)

    return buffer


@external
def includes(user: address) -> bool:
    self.must_be(msg.sender)

    return self.is_admin(user)


@external
def am_i() -> bool:
    return self.is_admin(msg.sender)


@external
def include(user: address):
    self.must_be(msg.sender)
    assert not self.is_admin(user), "User is already an admin."

    self.admins.append(user)


@external
def exclude(user: address):
    self.must_be(msg.sender)
    assert self.is_admin(user), "User is not an admin."

    buffer: DynArray[address, 256] = empty(DynArray[address, 256])

    for admin: address in self.admins:
        if admin != user:
            buffer.append(admin)

    self.admins = buffer

@view
def is_admin(user: address) -> bool:
    is_main: bool = user == self.main_admin
    is_sub: bool = user in self.admins
    return is_main or is_sub
