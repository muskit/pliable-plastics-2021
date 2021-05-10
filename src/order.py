## Order screen. Displays current orders in the DB, as well as allow creating new ones.
import curses
import npyscreen
from curseXcel import Table
from collections import namedtuple
import datetime

from utils import *
from menu import *
from structs import *

from customer import *
import material

class OrderForm(npyscreen.FormBaseNew):
    def __init__(self, newOrder: Order = None, *args, **kwargs):
        self.order = newOrder
        self.cust = self.order.customer if self.order != None else None
        self.material = self.order.design.material if self.order != None else None
        super(OrderForm, self).__init__(*args, **kwargs)

    def create(self):
        #self.myCust = self.add(npyscreen.TitleText, name = "Customer", value = self.order.phoneNum if self.order != None else "", begin_entry_at = 0, use_two_lines = True)
        self.add(npyscreen.FixedText, value = "Customer", editable = False)
        self.myCust = self.add(npyscreen.ButtonPress, name = "{} (#{})".format(self.cust.name, self.cust.id) if self.cust != None else ">>Select customer<<", when_pressed_function = self.set_customer)

        self.add(npyscreen.FixedText, value = "Design Details", editable = False, rely = 7)
        self.myDesc = self.add(npyscreen.TitleText, name = "Description", value = self.order.design.description if self.order != None else "", use_two_lines = True, begin_entry_at = 2)
        self.myFile = self.add(npyscreen.TitleText, name = "File", value = self.order.design.file if self.order != None else "", use_two_lines = True, rely = 11, begin_entry_at = 2)

        self.add(npyscreen.FixedText, value = "Material", rely = 14, editable = False)
        self.myMat = self.add(npyscreen.ButtonPress, name = self.material.name if self.order != None else ">>Select material<<", when_pressed_function = self.set_material)
        self.myApproxSize = self.add(npyscreen.TitleText, name = "kg mat. per product", value = self.order.design.approxSize if self.order != None else "", begin_entry_at = 2, use_two_lines = True)

        self.myQuantity = self.add(npyscreen.TitleText, name = "Quantity", value = self.order.quantity if self.order != None else "", rely = 19, begin_entry_at = 11)

        if self.order == None:
            self.name = "Creating an Order"
        else:
            self.name = "Editing order #{} (placed on {})".format(self.order.id, self.order.date)
            
        self.add(npyscreen.ButtonPress, name = "Save", rely = -4, when_pressed_function=self.save_order)
        self.add(npyscreen.ButtonPress, name = "Cancel", rely = -4, relx = 10, when_pressed_function = self.exit_editing)

    def save_order(self):
        order = self.get_order()
        database.push(order)
        self.exit_editing()

    def get_order(self):
        return Order(self.order.id if self.order != None else None,
                     self.order.date if self.order != None else datetime.date.today(),
                     self.cust,
                     Design(self.order.design.id if self.order != None else None,
                            self.myDesc.value,
                            self.myFile.value,
                            self.myApproxSize.value,
                            self.material),
                            self.myQuantity.value)
                        
    def set_customer(self):
        custScreen = curses.initscr()
        cl = CustomerListing(custScreen)
        self.cust = cl.loop(1)
        self.myCust.name = "{} (#{})".format(self.cust.name, self.cust.id) if self.cust != None else self.myCust.name
        self.display()

    def set_material(self):
        scr = curses.initscr()
        ml = material.MaterialListing(scr)
        self.material = ml.loop(True)
        self.myMat.name = self.material.name if self.material != None else self.myMat.name
        self.display()


# Orders table view. From here, we can create and modify orders.
class OrderListing:
    def __init__(self, screen):
        self.orderList = []

        self.screen = screen
        self.screenSize = self.screen.getmaxyx()
        self.tableWindow = self.screen.subwin(self.screenSize[0]-14, self.screenSize[1]-10, 4, 5)
        self.tableWinSize = self.tableWindow.getmaxyx()

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

    def loop(self, selectMode = False):
        key = None

        optionsWin = self.screen.subwin(2, self.tableWinSize[1], self.screenSize[0]-5, 5)
        options = Menu(optionsWin, "Options", [
            ("Select" if selectMode else "View/Edit", None),
            ("Place New Order", None),
            ("Refresh", None),
            ("Exit", None)
        ], False)

        while True:
            self.screen.clear()

            self.table.refresh()
            options.refresh()

            place_str(self.screen, 3,5, "--Orders--", True, True)
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
            
            if key in { curses.KEY_ENTER, 10, 13 } and self.table.cursor[0] > 0:
                order = self.orderList[self.table.cursor[0] - 1]
                if options.highlighted == 0: # View/Edit / Select
                    if selectMode:
                        return order
                    else:
                        of = OrderForm(order)
                        of.edit() 
                if options.highlighted == 1: # Place New Order
                    f = OrderForm()
                    f.edit()
                if options.highlighted == 2: # Refresh
                    self.refresh_table()
                if options.get_highlighted_text() == "Exit":
                    break
                self.refresh_table()