## All functions and classes related to Customer data.
import curses
import npyscreen
from curseXcel import Table
from copy import deepcopy

from utils import *
from menu import *

# object representing customer
class Customer:
    def __init__(self,
                 name = "",
                 phoneNum = "",
                 email = "",
                 streetAddress = "",
                 city = "",
                 state = "",
                 postalCode = "",
                 id = ""):
        self.name = name
        self.phoneNum = phoneNum
        self.email = email
        self.streetAddress = streetAddress
        self.city = city
        self.state = state
        self.postalCode = postalCode
        self.id = id

# customer modifcation/creation form (lib: npyscreen)
class CustomerForm(npyscreen.FormBaseNew):
    def __init__(self, newCust: Customer = None, *args, **kwargs):
        self.cust = deepcopy(newCust)
        super(CustomerForm, self).__init__(*args, **kwargs)
    def create(self):
        if self.cust == None:
            self.name = "Add new customer"

            self.myName = self.add(npyscreen.TitleText, name="Name", begin_entry_at = 0, use_two_lines = True)
            self.myPhoneNum = self.add(npyscreen.TitleText, name = "Phone Number", begin_entry_at = 0, use_two_lines = True, rely=5)
            self.myEmail = self.add(npyscreen.TitleText, name = "E-Mail Address", begin_entry_at = 0, use_two_lines = True)
            self.myStreetAddress = self.add(npyscreen.TitleText, name="Street Address", begin_entry_at = 0, use_two_lines = True, rely=10)
            self.myCity = self.add(npyscreen.TitleText, name="City", begin_entry_at = 0, use_two_lines = True, width = 15)
            self.myState = self.add(npyscreen.TitleText, name="State", begin_entry_at = 0, use_two_lines = True, max_width = 4, relx = 19, rely = 12)
            self.myPostalCode = self.add(npyscreen.TitleText, name="Postal Code", begin_entry_at = 0, use_two_lines = True)
            self.myID = None
        else:
            self.myName = self.add(npyscreen.TitleText, name="Name", value = self.cust.name, begin_entry_at = 0, use_two_lines = True)
            self.myPhoneNum = self.add(npyscreen.TitleText, name = "Phone Number", value = self.cust.phoneNum, begin_entry_at = 0, use_two_lines = True, rely=5)
            self.myEmail = self.add(npyscreen.TitleText, name = "E-Mail Address", value = self.cust.email, begin_entry_at = 0, use_two_lines = True)
            self.myStreetAddress = self.add(npyscreen.TitleText, name="Street Address", value = self.cust.streetAddress, begin_entry_at = 0, use_two_lines = True, rely=10)
            self.myCity = self.add(npyscreen.TitleText, name="City", value = self.cust.city, begin_entry_at = 0, use_two_lines = True, width = 15)
            self.myState = self.add(npyscreen.TitleText, name="State", value = self.cust.state, begin_entry_at = 0, use_two_lines = True, max_width = 4, relx = 19, rely = 12)
            self.myPostalCode = self.add(npyscreen.TitleText, name="Postal Code", value = self.cust.postalCode, begin_entry_at = 0, use_two_lines = True)
            self.myID = self.cust.id
            
            self.name = "Editing customer info for {} ({})".format(self.myName.value, self.myID)

        self.add(npyscreen.ButtonPress, name = "Save", rely = 17)
        self.add(npyscreen.ButtonPress, name = "Cancel", rely = 17, relx = 10, when_pressed_function = self.exit_editing)

        # TODO
        def save_customer(self):
            cust = get_customer()
            if cust.id == None: # create new Customer data
                pass
            else: # overwrite existing Customer data
                pass

        def get_customer(self):
            return Customer(self.myName,
                            self.myPhoneNum,
                            self.myEmail,
                            self.myStreetAddress,
                            self.myCity,
                            self.myState,
                            self.myPostalCode,
                            self.myID)

# Customers table view. From here, we can add and modify customers.
class CustomerListing:
    def __init__(self, screen):
        self.customerCount = 0
        self.customerList = []

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
            self.table.set_cell(idx, 4, "somewhere")
            
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