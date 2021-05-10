from collections import namedtuple

Customer = namedtuple("Customer", "id, name, phoneNum, email, streetAddress, city, state, postalCode")

Order = namedtuple("Order", "id, date, customer, design, quantity")
Design = namedtuple("Design", "id, description, file, approxSize, material")
Material = namedtuple("Material", "id, name, quantity, price, vendor")
Vendor = namedtuple("Vendor", "id, name, phoneNumber")

Shipment = namedtuple("Shipment", "id, order, carrier, totalPrice, dateBilled")