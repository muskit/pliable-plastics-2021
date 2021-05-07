import curses
from enum import Enum, auto

from utils import *
from menu import Menu
from customer import *

class State(Enum):
	EXIT = auto()
	CUSTOMER = auto()
	MODIFYCUST = auto()
	ORDER = auto()
	DESIGN = auto()
	PRODUCTION = auto()
	SHIPPING = auto()

def pp_main(screen):
	subWindow = screen.subwin(17, 3)
	login = Menu(subWindow, "--=Select a view=--", [
		("Orders", State.ORDER),
		("Customers", State.CUSTOMER),
		("Orders", State.ORDER),
		("Designs", State.DESIGN),
		("Production", State.PRODUCTION),
		("Shipping", State.SHIPPING),
		("Exit", State.EXIT)
	])

	sampleCust0 = Customer("Emlen Smales", "5254716325", "esmales1@exblog.jp", "5 Comanche Way", "Maple Plain", "MN", "55579", "231")
	sampleCust1 = Customer("Joe Mama", "6219897283", "wtf@example.net", "823 Bottom View Way", "Hell", "MI", "62266", "80")

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
			cl.add_customer(sampleCust0)
			cl.add_customer(sampleCust1)
			cl.loop()
		if state == State.MODIFYCUST:
			f = CustomerForm(sampleCust)
			f.edit()