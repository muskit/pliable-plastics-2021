# -*- coding: UTF-8 -*-
import curses

## Strings

# 61x13 company banner
banner = '''
██████╗ ██╗     ██╗ █████╗ ██████╗ ██╗     ███████╗         
██╔══██╗██║     ██║██╔══██╗██╔══██╗██║     ██╔════╝         
██████╔╝██║     ██║███████║██████╔╝██║     █████╗           
██╔═══╝ ██║     ██║██╔══██║██╔══██╗██║     ██╔══╝           
██║     ███████╗██║██║  ██║██████╔╝███████╗███████╗         
╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝         
                                                            
██████╗ ██╗      █████╗ ███████╗████████╗██╗ ██████╗███████╗
██╔══██╗██║     ██╔══██╗██╔════╝╚══██╔══╝██║██╔════╝██╔════╝
██████╔╝██║     ███████║███████╗   ██║   ██║██║     ███████╗
██╔═══╝ ██║     ██╔══██║╚════██║   ██║   ██║██║     ╚════██║
██║     ███████╗██║  ██║███████║   ██║   ██║╚██████╗███████║
╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝╚══════╝
'''
promptLogin = '''
 _______________
|  Select View  |
 ---------------
| 1. Customers  |
| 2. Orders     |
| 3. Shipping   |
 ---------------
'''

## Functions

# Allows placing a multi-line string at any point on
# the screen. It appears addstr()/insstr() does not
# use the x-coordinate argument, so this function is
# the workaround for that.
def place_str(screen, y: int, x: int, text, highlighted = False):
	text = str(text)
	arr = text.splitlines()
	for i in range(len(arr)):
		if highlighted:
			screen.addstr(y + i, x, arr[i], curses.A_REVERSE)
		else:
			screen.addstr(y + i, x, arr[i])