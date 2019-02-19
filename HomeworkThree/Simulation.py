#Gayathri Gude, Michael Yoshimura 
#OODA 4448 Homework Three
#Bruce Montgomery, Spring 2019

customer_max_tools = 3
store_max_tools = 20

class ToolCategory:
    def __init__(self, name):
        self._name = name

class Tool:
    def __init__(self, name, tool_cat):
        self._name = name
        self._tool_cat = tool_cat

class Inventory:
    def __init__(self, max_size):
        self._tools = []
        self._max_size = max_size

class CustomerType:
    def __init__(self, name, tool_amount, time_rented):
        self._name = name
        self._tool_amount = tool_amount
        self._time_rented = time_rented

class Customer:
    def __init__(self, name, customer_type):
        self._name = name
        self._inventory = Inventory(customer_max_tools)
        self._customer_type = customer_type

class Store:
    def __init__(self):
        self._customers = []
        self._inventory = Inventory(store_max_tools)

class Simulation:
    def __init__(self):
        self._days = 0
        self._store = Store()

simulation = Simulation()