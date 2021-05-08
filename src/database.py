
import mysql.connector
from mysql.connector import Error

from structs import *

def init():
    print("Connecting to database...")
    connection = create_connection("34.94.37.143", "root", "8OxcFylKtgEaxtll")

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
            pass
    globals()['dbConnection'].commit()

# Retrieve data and return converted structs (list)
def retrieve(dataType):
    if dataType == Customer: # return list of Customers
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