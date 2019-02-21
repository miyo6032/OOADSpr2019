#Gayathri Gude, Michael Yoshimura 
#OODA 4448 Homework Three
#Bruce Montgomery, Spring 2019

from random import randint

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

# Responsible for keeping track of tools and making sure there are no more tools than the max size
class Inventory:
    def __init__(self, max_size):
        self.tools = []
        self.max_size = max_size

    # Adds a new tool to the toolset
    # Returns whether the addition was successful
    def add_tool(self, tool):
        if not self.full():
            self.tools.append(tool)
            return True
        return False

    # Returns whether the remove was successful
    def remove_tool(self, tool):
        if tool in self.tools:
            self.tools.remove(tool)
            return True
        return False

    def full(self):
        return len(self.tools) == self.max_size - 1

    def empty(self):
        return len(self.tools) == 0

#NOTE customer should probably keep track of how long the tools have been rented, and when they should be returned
# The way this is set up couples a lot of attributes with customer type
# We assumed that because the tool renting was dependent on the customer
# type it would be okay, but if this every changed, we would be in trouble
class CustomerType:
    def __init__(self, type_name, tool_rent_min, tool_rent_max, time_rented_min, time_rented_max):
        self.type_name = type_name
        self.tool_rent_min = tool_rent_min
        self.tool_rent_max = tool_rent_max
        self.time_rented_min = time_rented_min
        self.time_rented_max = time_rented_max

    def __str__(self):
        return self.type_name

    def __repr__(self):
        return self.__str__()

# Responsible for 'going' to the store and either returning or renting tools when it is time
class Customer:
    def __init__(self, name, customer_type, customer_max_tools):
        self.name = name
        self.inventory = Inventory(customer_max_tools)
        self.customer_type = customer_type

    def can_rent_tools(self, tools):
        return len(tools) >= self.inventory.max_size and not self.inventory.full()

    # The customer is presented the tools from the store, and chooses some to rent
    def rent_tools(self, store):
        if not self.can_rent_tools(store.tools):
            print("Warning: could not rent tools to customer " + self.name)
        amount = randint(self.customer_type.tool_rent_min, self.customer_type.tool_rent_max)
        time = randint(self.customer_type.time_rented_min, self.customer_type.time_rented_max)
        for i in range(amount):
            store.rent_tool(randint(0, len(store.tools) - 1), time)

    # The customer returns each tool
    def return_tools(self, store):
        for tool in self.inventory.tools:
            self.inventory.remove_tool(tool)
            store.return_tool(tool)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

class Store:
    def __init__(self):
        self.customers = []
        self.inventory = Inventory(store_max_tools)

    def rent_tool(self, tool, time):
        pass

    def return_tool(self, tool):
        pass

class Simulation:
    def __init__(self):
        self.days = 0
        self.store = Store()

if __name__ == '__main__':
    pass