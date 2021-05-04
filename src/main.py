from ppclient import pp_main
import curses

def main():
	input("Resize terminal to desired size, then press enter to continue.")
	
	screen = curses.initscr()
	pp_main(screen)
	curses.endwin()
	# curses.wrapper(pp_main)

if __name__ == "__main__":
	main()