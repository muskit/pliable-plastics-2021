from utils import *
from enum import Enum, auto
import curses
from cursesmenu import SelectionMenu
from cursesmenu.items import *

class State(Enum):
	LOGIN = auto()

def login_menu():
	options = { "Order", "Process", "Shipping" }
	menu = SelectionMenu(options, title="Pliable Plastics Client")
	return menu

def pp_main(screen):
	key = -1
	login = login_menu()
	i = 0

	subWindow = screen.subwin(20, 3)
	login.screen = subWindow

	while True:
		curses.noecho()
		screen.clear()
		# Drawing
		place_str(screen, 1, 2, banner)
		place_str(screen, 18, 2, i)
		place_str(screen, 20, 3, key)
	
		subWindow.box('|', '-')
		subWindow.refresh()

		#set borders, draw screen
		screen.border('|', '|', '-', '-', '+', '+', '+', '+')
		screen.refresh()

		login.show()
		loginChoice = login.selected_item.text
		if loginChoice == "Exit":
			break