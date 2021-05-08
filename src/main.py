import ppclient
from curses import wrapper

import database

def main():
	database.init()
	print()

	# 2nd: if connection succeeds, start application
	input("Resize terminal to desired (preferably largest) size, then press ENTER to continue.\nDO NOT resize the terminal after pressing ENTER!")
	wrapper(ppclient.pp_main)

if __name__ == "__main__":
	main()