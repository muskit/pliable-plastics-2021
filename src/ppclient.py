import curses
from enum import Enum, auto

from utils import *
from menu import Menu
import database

from customer import *
from order import *
from material import *

class State(Enum):
	EXIT = auto()
	CUSTOMER = auto()
	ORDER = auto()
	DESIGN = auto()
	PRODUCTION = auto()
	SHIPPING = auto()
	MATERIALS = auto()

def pp_main(screen):
	globals()['winscr'] = screen
	subWindow = screen.subwin(17, 3)
	login = Menu(subWindow, "--=Select a view=--", [
		("Customers", State.CUSTOMER),
		("Orders", State.ORDER),
		# ("Designs", State.DESIGN),
		("Production", State.PRODUCTION),
		("Shipping", State.SHIPPING),
		("Manage Materials", State.MATERIALS),
		("Exit", State.EXIT)
	])

	sampleCust0 = Customer("99999", "Emlen Smales", "5254716325", "esmales1@exblog.jp", "5 Comanche Way", "Maple Plain", "MN", "55579")
	sampleCust1 = Customer("99999", "Joe Mama", "6219897283", "wtf@example.net", "823 Bottom View Way", "Hell", "MI", "62266")

	while True:
		# curses.noecho()
		screen.clear()
		
		# draw borders
		screen.border('|', '|', '-', '-', '+', '+', '+', '+')
		screen.refresh()

		# login
		place_str(screen, 1, 2, banner)
		screen.refresh()
		state = login.loop()

		# states
		if state == State.EXIT:
			break
		if state == State.CUSTOMER:
			cl = CustomerListing(screen)
			cl.loop()
		if state == State.ORDER:
			ol = OrderListing(screen)
			ol.loop()
		if state == State.MATERIALS:
			ml = MaterialListing(screen)
			ml.loop()