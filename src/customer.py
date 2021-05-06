## Customer data

import curses
import npyscreen
import copy

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
class CustomerForm(npyscreen.Form):
    def __init__(self, newCust: Customer = None, *args, **kwargs):
        self.cust = copy.deepcopy(newCust)
        self.myID = None
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

        def get_customer(self):
            return Customer(self.myName,
                            self.myPhoneNum,
                            self.myEmail,
                            self.myStreetAddress,
                            self.myCity,
                            self.myState,
                            self.myPostalCode,
                            self.myID)

# Customers table; from here, we can add and modify customers.
def CustomerListing():
    pass