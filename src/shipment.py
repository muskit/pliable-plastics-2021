## Order screen. Displays current orders in the DB, as well as allow creating new ones.
import curses
import npyscreen
from curseXcel import Table
from collections import namedtuple
import datetime
from decimal import Decimal, getcontext
from math import ceil

from utils import *
from menu import *
from structs import *
import database

import order

class ShipmentForm(npyscreen.FormBaseNew):
    def __init__(self, shipment: Shipment = None, *args, **kwargs):
        self.shipment = shipment
        self.order = shipment.order if shipment != None else None
        super(ShipmentForm, self).__init__(*args, **kwargs)
        self.name = "Editing shipment #{}".format(self.shipment.id) if shipment != None else "Add new shipment"

    def create(self):
        self.add(npyscreen.FixedText, value = "Order", editable = False)
        self.myOrder = self.add(npyscreen.ButtonPress, when_pressed_function = self.set_order)
        self.myOrderDesc = self.add(npyscreen.TitleFixedText, relx = 6, name = "Description", editable = False)
        self.myOrderMat = self.add(npyscreen.TitleFixedText, relx = 6, name = "Material", editable = False)
        self.myOrderSize = self.add(npyscreen.TitleFixedText, relx = 6, name = "Size/product", editable = False)
        self.myOrderQuantity = self.add(npyscreen.TitleFixedText, relx = 6, name = "Order Qty", editable = False)

        self.add(npyscreen.FixedText, value = "Ship to", editable = False, rely = 9)
        self.myCustName = self.add(npyscreen.FixedText, relx = 6, editable = False)
        self.myCustStreet = self.add(npyscreen.FixedText, relx = 6, editable = False)
        self.myCustCiStZip = self.add(npyscreen.FixedText, relx = 6, editable = False)
        
        self.myCarrier = self.add(npyscreen.TitleText, name = "Shipping Carrier", editable = True, rely = 14, begin_entry_at = 20)

        self.add(npyscreen.FixedText, value = "Total Bill", editable = False, rely = 16)
        self.myCostItem = self.add(npyscreen.TitleFixedText, relx = 6, name = "Item", editable = False, begin_entry_at = 26)
        self.myCostLabor = self.add(npyscreen.TitleFixedText, relx = 6, name = "Labor (35% of item)", editable = False, begin_entry_at = 26)
        self.myCostShip = self.add(npyscreen.TitleFixedText, relx = 6, name = "Shipping ($11 per 10kg)", editable = False, begin_entry_at = 26)
        self.myCostTotal = self.add(npyscreen.TitleFixedText,  name = "GRAND TOTAL", editable = False, begin_entry_at = 30)

        self.add(npyscreen.ButtonPress, name = "Save", rely = -4, when_pressed_function=self.save_shipment)
        self.add(npyscreen.ButtonPress, name = "Cancel", rely = -4, relx = 10, when_pressed_function = self.exit_editing)
        
        self.update_form_fields()


    def save_shipment(self):
        database.push(self.get_shipment())
        self.exit_editing()

    def get_shipment(self):
        if self.order != None:
            return Shipment(None, self.order, self.myCarrier.value, self.myCostTotal.value, datetime.date.today())

    def set_order(self):
        scr = curses.initscr()
        ol = order.OrderListing(scr)

        newOrder = ol.loop(True)
        if newOrder != None:
            self.order = newOrder
        self.update_form_fields()

    def update_form_fields(self):
        self.myOrder.name = "#{}".format(self.order.id) if self.order != None else ">>Select order<<"
        self.myOrderDesc.value = self.order.design.description if self.order != None else "NO ORDER SELECTED"
        self.myOrderMat.value = self.get_material_label() if self.order != None else "NO ORDER SELECTED"
        self.myOrderSize.value = self.order.design.approxSize if self.order != None else "NO ORDER SELECTED"
        self.myOrderQuantity.value = self.order.quantity if self.order != None else "NO ORDER SELECTED"

        self.myCustName.value = self.order.customer.name if self.order != None else "NO ORDER SELECTED"
        self.myCustStreet.value = self.order.customer.streetAddress if self.order != None else ""
        self.myCustCiStZip.value = "{}, {} {}".format(self.order.customer.city, self.order.customer.state, self.order.customer.postalCode) if self.order != None else ""
        
        self.myCostItem.name = "Item ({} x {} x {})".format(self.order.quantity, self.order.design.material.price, self.order.design.approxSize) if self.order != None else "NO ORDER SELECTED"
        self.myCostItem.value = str(round((Decimal(self.order.quantity) * Decimal(self.order.design.material.price)) * Decimal(self.order.design.approxSize), 2)) if self.order != None else "NO ORDER SELECTED"
        self.myCostLabor.value = str(round(0.35*float(self.myCostItem.value), 2)) if self.order != None else "NO ORDER SELECTED"
        self.myCostShip.value = "{:.2f}".format(11 * round(ceil(Decimal( Decimal(self.order.design.approxSize) * Decimal(self.order.quantity))/10 ))) if self.order != None else "NO ORDER SELECTED"

        self.myCostTotal.value = "{:.2f}".format(float(self.myCostItem.value) + float(self.myCostLabor.value) + float(self.myCostShip.value)) if self.order != None else "NO ORDER SELECTED"


        self.display()

    def get_material_label(self):
        if self.order != None:
            return "{} (${}/kg.)".format(self.order.design.material.name, float(self.order.design.material.price))
        else:
            return "NO ORDER SELECTED"




# Orders table view. From here, we can create and modify orders.
class ShipmentListing:
    def __init__(self, screen):
        self.shipmentList = []

        self.screen = screen
        self.screenSize = self.screen.getmaxyx()
        self.tableWindow = self.screen.subwin(self.screenSize[0]-14, self.screenSize[1]-10, 4, 5)
        self.tableWinSize = self.tableWindow.getmaxyx()

        self.optionsWin = self.screen.subwin(2, self.tableWinSize[1], self.screenSize[0]-5, 5)
        self.options = Menu(self.optionsWin, "Options", [
            ("Create New Shipment", None),
            ("Refresh", None),
            ("Exit", None)
        ], False)

        self.refresh_table()
        
    def refresh_table(self):
        self.shipmentList = database.retrieve(Shipment)
        self.regenerate_table()    

    def regenerate_table(self):
        cols = ['ID', 'Customer', 'Description', 'Date Billed/Shipped']
        self.table = create_table(self.tableWindow, cols, len(self.shipmentList))

        idx = 0
        for shipment in self.shipmentList:
            self.table.set_cell(idx, 0, shipment.id)
            self.table.set_cell(idx, 1, shipment.order.customer.name)
            self.table.set_cell(idx, 2, shipment.order.design.description)
            self.table.set_cell(idx, 3, shipment.dateBilled)
            idx += 1

        # get table cursor to appropriate spot
        self.table.cursor_down()
        self.table.cursor_down()

    def loop(self):
        key = None

        while True:
            self.screen.clear()

            self.table.refresh()
            self.options.refresh()

            place_str(self.screen, 3,5, "--Shipment History--", True, True)
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
                self.options.input(key)
            
            if key in { curses.KEY_ENTER, 10, 13 } and self.table.cursor[0] > 0:
                shipment = self.shipmentList[self.table.cursor[0] - 1]
                if self.options.highlighted == 0: # Create New Shipment
                    f = ShipmentForm()
                    f.edit()
                if self.options.highlighted == 1: # Refresh
                    self.refresh_table()
                if self.options.get_highlighted_text() == "Exit":
                    break
                self.refresh_table()