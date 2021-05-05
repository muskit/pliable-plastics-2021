from utils import *
from enum import Enum, auto
import curses
from login_menu import Menu

class State(Enum):
	EXIT = auto()
	LOGIN = auto()

def pp_main(screen):
	state = State.LOGIN
	subWindow = screen.subwin(20, 3)
	login = Menu(subWindow, "--=Select a view=--", [
		"Orders",
		"Customers",
		"Exit"
	])

	while True:
		# curses.noecho()
		screen.clear()
		
		# draw borders
		screen.border('|', '|', '-', '-', '+', '+', '+', '+')
		screen.refresh()

		# state
		if state == State.LOGIN:
			place_str(screen, 1, 2, banner)
			screen.refresh()
			login.loop()
			if login.get_selection_text() == "Exit":
				state = State.EXIT
		if state == State.EXIT:
			break