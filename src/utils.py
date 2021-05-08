# -*- coding: UTF-8 -*-
import curses
import curseXcel

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

def create_table(screen, cols: [str], rows, height_shorten_by = 0):
	dim = screen.getmaxyx()
	table = curseXcel.Table(screen, rows, len(cols), (dim[1]//len(cols)) - 1, dim[1], dim[0] - height_shorten_by, col_names = True, spacing = 1)

	idx = 0
	for col in cols:
		table.set_column_header(col, idx)
		idx += 1
	return table