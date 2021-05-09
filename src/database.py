
import mysql.connector
from mysql.connector import Error
import time
from curses import napms

from structs import *

def init():
    print("Connecting to database...")
    connection = create_connection("34.94.37.143", "root", "8OxcFylKtgEaxtll")# whitelisted

def create_connection(host_name, user_name, user_password):
    try:
        globals()['dbConnection'] = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
        return
    
    globals()['dbCursor'] = globals()['dbConnection'].cursor()
    globals()['dbCursor'].execute("USE main")

# Update/Insert to database
def push(obj):
    query = ""
    if type(obj) == Customer:
        if obj.id == None: # INSERTing (making new customer)
            queryCust = ("INSERT INTO Customers "
                         "(customer_name, phone_number, email) "
                         "VALUES ('{}','{}','{}')")
            queryAddr = ("INSERT INTO Addresses "
                         "(street_address, postal_code, state, city, customer_id) "
                         "VALUES ('{}','{}','{}','{}','{}')")
            
            globals()['dbCursor'].execute(queryCust.format(obj.name, obj.phoneNum, obj.email))
            custId = globals()['dbCursor'].lastrowid
            globals()['dbCursor'].execute(queryAddr.format(obj.streetAddress, obj.postalCode, obj.state, obj.city, custId))
        else: # UPDATEing
            queryCust = ("UPDATE Customers "
                         "SET customer_name = '{}', phone_number = '{}', email = '{}' "
                         "WHERE customer_id = '{}'")
            queryAddr = ("UPDATE Addresses "
                         "SET street_address = '{}', city = '{}', state = '{}', postal_code = '{}' "
                         "WHERE customer_id = '{}'")

            globals()['dbCursor'].execute(queryCust.format(obj.name, obj.phoneNum, obj.email, obj.id))
            globals()['dbCursor'].execute(queryAddr.format(obj.streetAddress, obj.city, obj.state, obj.postalCode, obj.id))
    elif type(obj) == Order:
        if obj.id == None: # Create new Order
            queryOrder = ("INSERT INTO Orders "
                         "(customer_name, phone_number, email) "
                         "VALUES ('{}','{}','{}')")
            queryDesign = ("INSERT INTO Addresses "
                         "(street_address, postal_code, state, city, customer_id) "
                         "VALUES ('{}','{}','{}','{}','{}')")
        else: # Update existing order
            queryOrder = ("UPDATE Orders "
                          "SET order_date = '{}', customer_id = '{}', design_id = '{}' "
                          "WHERE order_id = '{}'")
            queryDesign = ("UPDATE Design "
                           "SET description = '{}', file = '{}', approx_size = '{}', material_id = '{}' "
                           "WHERE design_id = '{}' ")

            globals()['dbCursor'].execute(queryDesign.format(obj.design.description, obj.design.file, obj.design.approxSize, obj.design.material.id, obj.design.id))
            globals()['dbCursor'].execute(queryOrder.format(obj.date, obj.customer.id, obj.design.id, obj.id))

    globals()['dbConnection'].commit()

# Retrieve data and return converted structs
def retrieve(dataType, searchId = None):
    if dataType == Customer: # return type Customers
       return get_customer(searchId)
    elif dataType == Order:
        return get_order(searchId)
    elif dataType == Material:
        return get_material(searchId)

def get_customer(searchId = None):
    if searchId == None: # list
        globals()['dbCursor'].execute('SELECT * FROM Customers')
        custs = globals()['dbCursor'].fetchall()

        ret = []
        for (id, name, phone, email) in custs:
            globals()['dbCursor'].execute("SELECT street_address, city, state, postal_code "
                                        "FROM Addresses "
                                        "WHERE customer_id = {}".format(id))
            curAddr = globals()['dbCursor'].fetchone()
            ret.append(Customer(id, name, phone, email, curAddr[0], curAddr[1], curAddr[2], str(curAddr[3])))

        return ret
    else: # object by searchId
        globals()['dbCursor'].execute('SELECT * FROM Customers ' 
                                        'WHERE customer_id = {}'.format(searchId))
        cust = globals()['dbCursor'].fetchone()

        globals()['dbCursor'].execute("SELECT street_address, city, state, postal_code "
                                        "FROM Addresses "
                                        "WHERE customer_id = {}".format(searchId))
        addr = globals()['dbCursor'].fetchone()

        return Customer(cust[0], cust[1], cust[2], cust[3], addr[0], addr[1], addr[2], str(addr[3]))

def get_vendor(searchId = None):
    if searchId == None:
        pass
    else:
        globals()['dbCursor'].execute('SELECT * FROM Vendor WHERE vendor_id = {}'.format(searchId))
        rowVendor = globals()['dbCursor'].fetchone()
        return Vendor(rowVendor[0], rowVendor[1], rowVendor[2])

def get_material(searchId = None):
    if searchId == None:
        globals()['dbCursor'].execute('SELECT * FROM Materials')
        ret = []

        for (id, name, vendor_id, quantity, price) in globals()['dbCursor']:
            ret.append(Material(id, name, quantity, price, get_vendor(vendor_id)))
        return ret
    else:
        globals()['dbCursor'].execute('SELECT * FROM Materials WHERE material_id = {}'.format(searchId))
        rowMaterial = globals()['dbCursor'].fetchone()
        return Material(rowMaterial[0], rowMaterial[1], rowMaterial[3], rowMaterial[4], get_vendor(rowMaterial[2]))

def get_design(searchId = None):
    if searchId == None: # list
        pass
    else:
        globals()['dbCursor'].execute('SELECT * FROM Design WHERE design_id = {}'.format(searchId))
        rowDesign = globals()['dbCursor'].fetchone()
        return Design(rowDesign[0], rowDesign[1], rowDesign[2], str(rowDesign[3]), get_material(rowDesign[4]))

def get_order(searchId = None):
    if searchId == None: # list
        globals()['dbCursor'].execute('SELECT * FROM Orders')
        orders = globals()['dbCursor'].fetchall()

        ret = []
        for rowOrder in orders:
            # globals()['dbCursor'].execute('SELECT * FROM Design WHERE design_id = {}'.format(rowOrder[3]))
            # rowDesign = globals()['dbCursor'].fetchone()
            # globals()['dbCursor'].execute('SELECT * FROM Materials WHERE material_id = {}'.format(rowDesign[4]))
            # rowMaterial = globals()['dbCursor'].fetchone()
            # globals()['dbCursor'].execute('SELECT * FROM Vendor WHERE vendor_id = {}'.format(rowMaterial[2]))
            # rowVendor = globals()['dbCursor'].fetchone()

            design = get_design(rowOrder[3])
            ret.append(Order(rowOrder[0], rowOrder[1], design, get_customer(rowOrder[2])))
        
        return ret
    else: # object by searchId
        pass