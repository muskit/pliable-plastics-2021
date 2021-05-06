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
		("Modify Customer Test", State.MODIFYCUST),
		("Orders", State.ORDER),
		("Designs", State.DESIGN),
		("Production", State.PRODUCTION),
		("Shipping", State.SHIPPING),
		("Exit", State.EXIT)
	])

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
			f = CustomerForm()
			f.edit()
		if state == State.MODIFYCUST:
			cust = Customer("Emlen Smales", "5254716325", "esmales1@exblog.jp", "5 Comanche Way", "Maple Plain", "MN", "55579", "231")
			f = CustomerForm(cust)
			f.edit()