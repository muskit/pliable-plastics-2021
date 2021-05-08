from collections import namedtuple

Customer = namedtuple("Customer", "id, name, phoneNum, email, streetAddress, city, state, postalCode")

Order = namedtuple("Order", "id, description, orderDate, customerId, designId")
Design = namedtuple("Design", "id, description, version, file, approxSize, matId")
Material = namedtuple("Material", "id, name, quantity")