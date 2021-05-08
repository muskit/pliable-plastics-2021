## Order screen. Displays current orders in the DB, as well as allow creating new ones.
import curses
import npyscreen
from curseXcel import Table
from collections import namedtuple

from utils import *
from menu import *
from customer import *
from structs import *


class OrderForm(npyscreen.FormBaseNew):
    def __init__(self, newOrder: Order = None, *args, **kwargs):
        self.order = newOrder
        self.cust = self.order.customer if self.order != None else None
        super(OrderForm, self).__init__(*args, **kwargs)

    def create(self):
        #self.myCust = self.add(npyscreen.TitleText, name = "Customer", value = self.order.phoneNum if self.order != None else "", begin_entry_at = 0, use_two_lines = True)
        self.add(npyscreen.FixedText, value = "Customer", editable = False)
        self.myCust = self.add(npyscreen.ButtonPress, name = self.cust.name if self.cust != None else "Select a customer", when_pressed_function = self.set_customer)

        self.add(npyscreen.FixedText, value = "Design Details", editable = False, rely = 8)
        self.myDesc = self.add(npyscreen.TitleText, name = self.order.design.description if self.order != None else "Description", value = self.order.description if self.order != None else "")
        self.myFile = self.add(npyscreen.TitleText, name = self.order.design.file if self.order != None else "File", value = "")

        self.add(npyscreen.FixedText, value = "Material", rely = 13, editable = False)
        self.myMat = self.add(npyscreen.ButtonPress, name = self.order.design.material.name if self.order != None else "Select material", when_pressed_function = self.set_material)
        self.myQuantity = self.add(npyscreen.TitleText, name = "Quantity", value = self.order.design.approxSize if self.order != None else "")

        if self.order == None:
            self.name = "Creating an Order"
        else:
            self.name = "Editing order {} (placed on {})".format(self.order.id, self.order.orderDate)
            
        self.add(npyscreen.ButtonPress, name = "Save", rely = -4)
        self.add(npyscreen.ButtonPress, name = "Cancel", rely = -4, relx = 10, when_pressed_function = self.exit_editing)

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
                        
    def set_customer(self):
        custScreen = curses.initscr()
        cl = CustomerListing(custScreen)
        self.cust = cl.loop(1)
        self.myCust.name = "{} ({})".format(self.cust.name, self.cust.id) if self.cust != None else "No Customer"
        self.DISPLAY()

    def set_material(self):
        pass


# Orders table view. From here, we can create and modify orders.
class OrderListing:
    def __init__(self, screen):
        self.orderList = []

        self.screen = screen
        self.screenSize = self.screen.getmaxyx()
        self.tableWindow = self.screen.subwin(self.screenSize[0]-14, self.screenSize[1]-10, 4, 5)
        self.tableWinSize = self.tableWindow.getmaxyx()

        self.optionsWin = self.screen.subwin(2, self.tableWinSize[1], self.screenSize[0]-5, 5)
        self.options = Menu(self.optionsWin, "Options", [
            ("View/Edit", None),
            ("Place New Order", None),
            ("Exit", None)
        ], False)

        self.refresh_table()
        
    def refresh_table(self):
        self.orderList = database.retrieve(Order)
        self.regenerate_table()    

    def regenerate_table(self):
        cols = ['ID', 'Customer', 'Description', 'Order Placed']
        self.table = create_table(self.tableWindow, cols, len(self.orderList))

        idx = 0
        for order in self.orderList:
            self.table.set_cell(idx, 0, order.id)
            self.table.set_cell(idx, 1, order.customer.name)
            self.table.set_cell(idx, 2, order.design.description)
            self.table.set_cell(idx, 3, order.date)
            idx += 1

        # get table cursor to appropriate spot
        self.table.cursor_down()
        self.table.cursor_down()

    def loop(self):
        key = None

        while True:
            self.screen.clear()

            self.table.refresh()
            # place_str(self.screen, 30,5, str(key), highlight=True)
            self.options.refresh()

            place_str(self.screen, 3,5, "--Order History--", True, True)
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
                    pass
                if self.options.highlighted == 1: # Place New Order
                    f = OrderForm()
                    f.edit()
                if self.options.get_highlighted_text() == "Exit":
                    break