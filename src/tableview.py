import curses
import curseXcel

class CustomerListing:
    def __init__(self, screen):
        self.customerList = []

        self.screen = screen
        self.screenSize = self.screen.getmaxyx()
        self.tableWindow = self.screen.subwin(self.screenSize[0]-14, self.screenSize[1]-10, 4, 5)
        self.tableWinSize = self.tableWindow.getmaxyx()

        self.refresh_table()

    def refresh_table(self):
        # TODO: Retrieve data
        self.regenerate_table()        

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

    # modes: 0 = creation/edit, 1 = selection; shoudl return a Customer obj
    def loop(self, mode = 0):
        key = None
        optionsWin = self.screen.subwin(2, self.tableWinSize[1], self.screenSize[0]-10, 5)
        options = Menu(optionsWin, "Options", [
            ("View/Edit" if mode == 0 else "Select", None),
            ("Add New Customer", None),
            ("Exit", None)
        ], False)
        while True:
            self.screen.clear()
            self.table.refresh()
            options.refresh()

            place_str(self.screen, 3,5, "--Customer Data--" if mode == 0 else "--Select a customer--", True, True)
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
                    if mode == 0:
                        f = CustomerForm()
                        f.edit()
                    else:
                        return customer
                if options.highlighted == 1: # Add New Customer
                    f = CustomerForm()
                    f.edit()
                if options.get_highlighted_text() == "Exit":
                    break