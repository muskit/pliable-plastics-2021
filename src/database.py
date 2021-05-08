
import mysql.connector
from mysql.connector import Error

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

# Update/Create in database
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

    globals()['dbConnection'].commit()

def get_customer(searchId):
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

def get_order(searchId):
    if searchId == None: # list
        globals()['dbCursor'].execute('SELECT * FROM Orders')
        orders = globals()['dbCursor'].fetchall()

        globals()['dbCursor'].execute('SELECT * FROM Design')
        designs = globals()['dbCursor'].fetchall()

        globals()['dbCursor'].execute('SELECT * FROM Materials')
        materials = globals()['dbCursor'].fetchall()

        ret = []
        for rowOrder in orders:
            globals()['dbCursor'].execute('SELECT * FROM Design WHERE design_id = {}'.format(rowOrder[3]))
            rowDesign = globals()['dbCursor'].fetchone()
            globals()['dbCursor'].execute('SELECT * FROM Materials WHERE material_id = {}'.format(rowDesign[4]))
            rowMaterial = globals()['dbCursor'].fetchone()

            material = Material(rowMaterial[0], rowMaterial[1], rowMaterial[3], rowMaterial[4])
            design = Design(rowDesign[0], rowDesign[1], rowDesign[2], rowDesign[3], material)
            ret.append(Order(rowOrder[0], rowOrder[1], design, get_customer(rowOrder[2])))
        
        return ret
    else: # object by searchId
        pass

# Retrieve data and return converted structs
def retrieve(dataType, searchId = None):
    if dataType == Customer: # return type Customers
       return get_customer(searchId)
    elif dataType == Order:
        return get_order(searchId)