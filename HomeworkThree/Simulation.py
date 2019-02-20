#Gayathri Gude, Michael Yoshimura 
#OODA 4448 Homework Three
#Bruce Montgomery, Spring 2019

customer_max_tools = 3
store_max_tools = 20

# A tool category is responsible for the tool's price
class ToolCategory:
    def __init__(self, category_name, price):
        self.category_name = category_name
        self.price = price

    def __str__(self):
        return self.category_name

    def __repr__(self):
        return self.__str__()

# A tool is not responsible for anything except for its category and name
class Tool:
    def __init__(self, tool_name, tool_cat):
        self.tool_name = tool_name
        self.category = tool_cat

    def __str__(self):
        return self.tool_name

    def __repr__(self):
        return self.__str__()

class Inventory:
    def __init__(self, max_size):
        self.tools = []
        self.max_size = max_size

#NOTE customer should probably keep track of how long the tools have been rented, and when they should be returned
class CustomerType:
    def __init__(self, name, tool_amount, time_rented):
        self.name = name
        self.tool_amount = tool_amount
        self.time_rented = time_rented

class Customer:
    def __init__(self, name, customer_type):
        self.name = name
        self.inventory = Inventory(customer_max_tools)
        self.customer_type = customer_type

class Store:
    def __init__(self):
        self.customers = []
        self.inventory = Inventory(store_max_tools)

class Simulation:
    def __init__(self):
        self.days = 0
        self.store = Store()

if __name__ == '__main__':
    pass