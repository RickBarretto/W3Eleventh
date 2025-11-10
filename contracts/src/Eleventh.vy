import Admins
import Cards
import Inventory
import Rewardings
import Trades

initializes: Admins
initializes: Inventory

@deploy
def __init__():
    Admins.__init__()
    Inventory.__init__()
