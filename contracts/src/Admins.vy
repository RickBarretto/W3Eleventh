
main_admin: address
admins: DynArray[address, 256]


@deploy
def __init__():
    self.main_admin = msg.sender


@view
@external
def all() -> DynArray[address, 257]:
    buffer: DynArray[address, 257] = empty(DynArray[address, 257])

    buffer.append(self.main_admin)
    for admin: address in self.admins:
        buffer.append(admin)

    return buffer


@external
def includes(user: address) -> bool:
    return self.is_admin(user)


@external
def am_i() -> bool:
    return self.is_admin(msg.sender)


@external
def include(user: address):
    assert self.is_admin(msg.sender), "Only admins can include new admins."
    assert not self.is_admin(user), "User is already an admin."

    self.admins.append(user)


@external
def exclude(user: address):
    assert self.is_admin(msg.sender), "Only admins can exclude admins."
    assert self.is_admin(user), "User is not an admin."

    buffer: DynArray[address, 256] = empty(DynArray[address, 256])

    for admin: address in self.admins:
        if admin != user:
            buffer.append(admin)

    self.admins = buffer


def is_admin(user: address) -> bool:
    is_main: bool = user == self.main_admin
    is_sub: bool = user in self.admins
    return is_main or is_sub
