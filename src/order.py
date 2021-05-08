## Order screen. Displays current orders in the DB, as well as allow creating new ones.
import curses
import npyscreen
from curseXcel import Table
from copy import deepcopy

from utils import *
from menu import *
from customer import *
from collections import namedtuple

from structs import *

# customer modifcation/creation form (lib: npyscreen)
class OrderForm(npyscreen.FormBaseNew):
    def __init__(self, newOrder: Order = None, *args, **kwargs):
        self.order = deepcopy(newOrder)
        super(OrderForm, self).__init__(*args, **kwargs)
    def create(self):
        self.myOrderDate = self.add(npyscreen.TitleText, name = "Phone Number", value = self.order.phoneNum if self.order != None else "", begin_entry_at = 0, use_two_lines = True, rely=5)
        self.myCustId = self.add(npyscreen.TitleText, name = "E-Mail Address", value = self.order.email if self.order != None else "", begin_entry_at = 0, use_two_lines = True)
        self.myDesignId = self.add(npyscreen.TitleText, name="Street Address", value = self.order.streetAddress if self.order != None else "", begin_entry_at = 0, use_two_lines = True, rely=10)

        if self.order == None:
            self.name = "Creating an Order"
        else:
            self.name = "Editing order {}".format(self.myID)
            
        self.add(npyscreen.ButtonPress, name = "Save", rely = 17)
        self.add(npyscreen.ButtonPress, name = "Cancel", rely = 17, relx = 10, when_pressed_function = self.exit_editing)

        # TODO
        def save_order(self):
            order = get_order()
            if order.id == None: # create new order
                pass
            else: # update existing order
                pass

        def get_order(self):
            return Order(self.Id,
                         self.myOrderDate,
                         self.myCustId,
                         self.myDesignId)

# Orders table view. From here, we can create and modify orders.
class OrderListing:
    def __init__(self, screen):
        self.orderList = []

        self.screen = screen
        self.screenSize = self.screen.getmaxyx()
        self.tableWindow = self.screen.subwin(self.screenSize[0]-14, self.screenSize[1]-10, 4, 5)
        self.tableWinSize = self.tableWindow.getmaxyx()

        self.regenerate_table()

        self.optionsWin = self.screen.subwin(2, self.tableWinSize[1], self.screenSize[0]-10, 5)
        self.options = Menu(self.optionsWin, "Options", [
            ("View/Edit", None),
            ("Add New Customer", None),
            ("Exit", None)
        ], False)
        
    def refresh_table(self):
        # TODO: Retrieve data
        regenerate_table()    

    def regenerate_table(self):
        self.table = Table(self.tableWindow, len(self.customerList), 5, (self.tableWinSize[1]//5) - 3, self.tableWinSize[1], self.tableWinSize[0] - 3, col_names = True, spacing = 1)

        self.table.set_column_header("ID", 0)
        self.table.set_column_header("Name", 1)
        self.table.set_column_header("Phone Number", 2)
        self.table.set_column_header("E-mail Address", 3)
        self.table.set_column_header("City/State", 4)

        idx = 0
        for cust in self.customerList:
            self.table.set_cell(idx, 0, cust.id)
            self.table.set_cell(idx, 1, cust.name)
            self.table.set_cell(idx, 2, cust.phoneNum)
            self.table.set_cell(idx, 3, cust.email)
            self.table.set_cell(idx, 4, "{}, {}}".format(cust.city, cust.state))
            
            idx += 1

        # get table cursor to appropriate spot
        self.table.cursor_down()
        self.table.cursor_down()

    def add_customer(self, newCust: Customer):
        if newCust != None and type(newCust) == Customer:
            print("Adding new customer {}".format(newCust.id))
            self.customerList.append(deepcopy(newCust))
            self.regenerate_table()

    def loop(self):
        key = None

        while True:
            self.screen.clear()

            self.table.refresh()
            # place_str(self.screen, 30,5, str(key), highlight=True)
            self.options.refresh()

            place_str(self.screen, 3,5, "--Customer Data--", True, True)
            self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')
            # self.tableWindow.box('|', '-')
            # self.optionsWin.box('|', '-')
            self.screen.refresh()
            
            # Input
            key = self.screen.getch()
            if key == ord('q'):
                return
            
            if key == curses.KEY_UP:
                self.table.cursor_up()
            if key == curses.KEY_DOWN:
                self.table.cursor_down()
            if key in {curses.KEY_LEFT, curses.KEY_RIGHT}:
                self.options.input(key)
            
            if key in { curses.KEY_ENTER, 10, 13 }:
                if self.options.highlighted == 0: # View/Edit
                    f = CustomerForm(self.customerList[self.table.cursor[0] - 1])
                    f.edit()
                if self.options.highlighted == 1: # Add New Customer
                    f = CustomerForm()
                    f.edit()
                if self.options.get_highlighted_text() == "Exit":
                    break