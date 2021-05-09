## All functions and classes related to Customer data.
import curses
import npyscreen
from curseXcel import Table
from copy import deepcopy

from utils import *
from menu import *
from structs import *
import database

# customer modifcation/creation form (lib: npyscreen)
class CustomerForm(npyscreen.FormBaseNew):
    def __init__(self, newCust: Customer = None, *args, **kwargs):
        self.cust = newCust
        super(CustomerForm, self).__init__(*args, **kwargs)
    def create(self):
        self.myName = self.add(npyscreen.TitleText, name="Name", value = self.cust.name if self.cust != None else "", begin_entry_at = 0, use_two_lines = True)
        self.myPhoneNum = self.add(npyscreen.TitleText, name = "Phone Number", value = self.cust.phoneNum if self.cust != None else "", begin_entry_at = 0, use_two_lines = True, rely=5)
        self.myEmail = self.add(npyscreen.TitleText, name = "E-Mail Address", value = self.cust.email if self.cust != None else "", begin_entry_at = 0, use_two_lines = True)
        self.myStreetAddress = self.add(npyscreen.TitleText, name="Street Address", value = self.cust.streetAddress if self.cust != None else "", begin_entry_at = 0, use_two_lines = True, rely=10)
        self.myCity = self.add(npyscreen.TitleText, name="City", value = self.cust.city if self.cust != None else "", begin_entry_at = 0, use_two_lines = True, width = 15)
        self.myState = self.add(npyscreen.TitleText, name="State", value = self.cust.state if self.cust != None else "", begin_entry_at = 0, use_two_lines = True, max_width = 4, relx = 19, rely = 12)
        self.myPostalCode = self.add(npyscreen.TitleText, name="Postal Code", value = self.cust.postalCode if self.cust != None else "", begin_entry_at = 0, use_two_lines = True)
        self.myID = self.cust.id if self.cust != None else None

        if self.cust == None:
            self.name = "Add new customer"
        else:
            self.name = "Editing customer info for {} ({})".format(self.myName.value, self.myID)

        self.add(npyscreen.ButtonPress, name = "Save", rely = -4, when_pressed_function = self.save_customer)
        self.add(npyscreen.ButtonPress, name = "Cancel", rely = -4, relx = 10, when_pressed_function = self.exit_editing)

    # TODO
    def save_customer(self):
        cust = self.get_customer()
        database.push(cust)
        self.exit_editing()

    def get_customer(self):
        return Customer(self.myID if self.myID != None else None,
                        self.myName.value,
                        self.myPhoneNum.value,
                        self.myEmail.value,
                        self.myStreetAddress.value,
                        self.myCity.value,
                        self.myState.value,
                        self.myPostalCode.value)

# Customers table view. From here, we can add, modify, and retrieve customers.
class CustomerListing:
    def __init__(self, screen):
        self.customerList = []

        self.screen = screen
        self.screenSize = self.screen.getmaxyx()
        self.tableWindow = self.screen.subwin(self.screenSize[0]-14, self.screenSize[1]-10, 4, 5)
        self.tableWinSize = self.tableWindow.getmaxyx()

        self.refresh_table()

    def refresh_table(self):
        self.customerList = database.retrieve(Customer)
        self.regenerate_table()        

    def regenerate_table(self):
        cols = ['ID', 'Name', 'Phone Number', 'E-Mail Address', 'City/State']
        # self.table = Table(self.tableWindow, len(self.customerList), 5, (self.tableWinSize[1]//5) - 1, self.tableWinSize[1], self.tableWinSize[0] - 3, col_names = True, spacing = 1)
        self.table = create_table(self.tableWindow, cols, len(self.customerList))

        # self.table.set_column_header("ID", 0)
        # self.table.set_column_header("Name", 1)
        # self.table.set_column_header("Phone Number", 2)
        # self.table.set_column_header("E-mail Address", 3)
        # self.table.set_column_header("City/State", 4)

        idx = 0
        for cust in self.customerList:
            self.table.set_cell(idx, 0, cust.id)
            self.table.set_cell(idx, 1, cust.name)
            self.table.set_cell(idx, 2, cust.phoneNum)
            self.table.set_cell(idx, 3, cust.email)
            self.table.set_cell(idx, 4, "{}, {}".format(cust.city, cust.state))
            
            idx += 1

        # get table cursor to appropriate spot
        self.table.cursor_down()
        self.table.cursor_down()

    def add_customer(self, newCust: Customer):
        if newCust != None and type(newCust) == Customer:
            self.customerList.append(deepcopy(newCust))
            self.regenerate_table()

    # modes: 0 = creation/edit, 1 = selection (should return a Customer obj)
    def loop(self, selectMode = 0):
        key = None
        optionsWin = self.screen.subwin(2, self.tableWinSize[1], self.screenSize[0]-5, 5)
        optionsList = [
            ("View/Edit" if selectMode else "Select", None),
            ("Add New Customer", None),
            ("Refresh", None),
            ("Exit", None)
        ]
        options = Menu(optionsWin, "Options", optionsList, False)
        while True:
            self.screen.clear()
            self.table.refresh()
            options.refresh()

            place_str(self.screen, 3,5, "--Customer Data--" if selectMode else "--Select a customer--", True, True)
            self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')
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
                options.input(key)
            
            if key in { curses.KEY_ENTER, 10, 13 }:
                if options.highlighted == 0 and self.table.cursor[0] > 0: # View/Edit / Select
                    customer = self.customerList[self.table.cursor[0] - 1]
                    if selectMode:
                        f = CustomerForm(customer)
                        f.edit()
                        self.refresh_table()
                    else: # Select mode
                        return customer
                if options.highlighted == 1: # Add New Customer
                    f = CustomerForm()
                    f.edit()
                    self.refresh_table()
                if options.highlighted == 2: # Refresh
                    self.refresh_table()
                if options.get_highlighted_text() == "Exit":
                    break