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

## Functions

# Allows placing a multi-line string at any point on
# the screen. It appears addstr()/insstr() does not
# use the x-coordinate argument, so this function is
# the workaround for that.
def place_str(screen, y: int, x: int, text, bold = False, highlight = False):
	text = str(text)
	arr = text.splitlines()

	attr = 0
	if highlight:
		attr = attr | curses.A_REVERSE
	if bold:
		attr = attr | curses.A_BOLD

	for i in range(len(arr)):
		screen.addstr(y + i, x, arr[i], attr)