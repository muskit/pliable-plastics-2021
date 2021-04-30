from __init__ import *
from enum import Enum, auto
import time
import curses

class State(Enum):
	LOGIN = auto()

def main():
	screen = curses.initscr()

	while True:
		key = screen.getkey()
		screen.clear()
		screen.addstr(0, 0, banner)
		screen.addstr(35, 10, key)
		screen.refresh()

		if key == 'KEY_Z':
			break

		curses.napms(100)
	
	curses.endwin()

	print("Window ended.")

if __name__ == "__main__":
	main()