import curses
import curseXcel
import npyscreen
from enum import Enum, auto

from menu import *
from utils import *
import database

class MenuChoice(Enum):
    SELECT = auto()
    EDIT = auto()
    ADD = auto()
    EXIT = auto()

class MaterialListing:
    def __init__(self, screen, selectMode = False):
        self.materialList = []
        
        self.screen = screen
        self.screenSize = self.screen.getmaxyx()
        self.tableWindow = self.screen.subwin(self.screenSize[0]-14, self.screenSize[1]-10, 4, 5)
        self.tableWinSize = self.tableWindow.getmaxyx()
        self.optionsWin = self.screen.subwin(2, self.tableWinSize[1], self.screenSize[0]-5, 5)

        self.refresh_table()

    def refresh_table(self):
        self.materialList = database.get_material()
        self.regenerate_table()

    def regenerate_table(self):
        tableCols = ['ID', 'Name', 'Price', 'Quantity', 'Vendor']
        self.table = create_table(self.tableWindow, tableCols, len(self.materialList))
        
        idx = 0
        for mat in self.materialList:
            self.table.set_cell(idx, 0, mat.id)
            self.table.set_cell(idx, 1, mat.name)
            self.table.set_cell(idx, 2, mat.price)
            self.table.set_cell(idx, 3, mat.quantity)
            self.table.set_cell(idx, 4, "{} (#{})".format(mat.vendor.name, mat.vendor.id))
        self.table.cursor_down()
        self.table.cursor_down()

    def loop(self, selectMode = False):
        menuOptions = [
            ('Select', MenuChoice.SELECT) if selectMode else ('View/Edit', MenuChoice.EDIT),
            ('Add New Material', MenuChoice.ADD),
            ('Exit', MenuChoice.EXIT)
        ]
        menu = Menu(self.optionsWin, '', menuOptions, False)
        
        self.refresh_table()

        while True:
            self.screen.clear()
            self.table.refresh()
            menu.refresh()
            
            place_str(self.screen, 3,5, "--Manage Materials--", True, True)
            self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')

            key = self.screen.getch()
            if key == curses.KEY_UP:
                self.table.cursor_up()
            if key == curses.KEY_DOWN:
                self.table.cursor_down()
            if key in {curses.KEY_LEFT, curses.KEY_RIGHT}:
                menu.input(key)
            
            if key in { curses.KEY_ENTER, 10, 13 } and self.table.cursor[0] > 0:
                mat = self.materialList[self.table.cursor[0] - 1]
                if menu.get_highlighted_text() == "Exit":
                    break