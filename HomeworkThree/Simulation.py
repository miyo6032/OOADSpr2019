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

# Responsible for keeping track of a rental, which contains rental day and cost
class Rental:
    def __init__(self, tools, start_date, return_date):
        self.tools = tools
        self.return_date = return_date
        self.start_date = start_date

    def days_rented(self):
        return self.return_date - self.start_date

    def cost(self):
        cost_per_day = sum([tool.category.price for tool in self.tools])
        return self.days_rented() * cost_per_day

    def __str__(self):
        return "Rental Info: " + len(self.tools) + " tools for " + self.days_rented() + " days for $" + self.cost()

    def __repr__(self):
        return self.__str__()

# This Customertype design this is set up couples a lot of attributes with customer type
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
    def __init__(self, name, customer_type):
        self.name = name
        self.active_rentals = []
        self.customer_type = customer_type

    def get_tools_rented(self):
        return sum([len(rental.tools) for rental in self.active_rentals])

    # If the customer can rent more tools, and if there are tools left to rent from the store
    # NOTE: Having a customer have to know about the store may not be the greatest thing
    def can_rent_tools(self, store):
        return len(store.inventory.tools) >= self.customer_type.tool_rent_max and self.get_tools_rented() < customer_max_tools

    # The customer is presented the tools from the store, and chooses some to rent
    def rent_tools(self, store, current_date):
        if not self.can_rent_tools(store.tools):
            print("Warning: could not rent tools to customer " + self.name)
        amount = randint(self.customer_type.tool_rent_min, self.customer_type.tool_rent_max)
        tools_to_rent = [randint(0, len(store.tools) - 1) for i in range(amount)]
        rent_time = randint(self.customer_type.time_rented_min, self.customer_type.time_rented_max)
        rental = Rental(tools_to_rent, current_date, current_date + rent_time)
        store.make_rental(rental)
        self.active_rentals.append(rental)

    # The customer returns each tool, and the store is updated as well
    def return_tools(self, store, current_date):
        for rental in self.active_rentals:
            if rental.return_date == current_date:
                store.return_rental(rental)
                self.active_rentals.remove(rental)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

class Store:
    def __init__(self):
        self.customers = []
        self.inventory = Inventory(store_max_tools)
        self.money = 0
        self.complete_rentals = []
        self.active_rentals = []

    # Process the rental request made by the customer
    def make_rental(self, rental):
        self.money += rental.cost()
        for tool in rental.tools:
            self.inventory.remove_tool(tool)
        self.active_rentals.append(rental)

    # Recieve the tools and complete the rental
    def return_rental(self, rental):
        for tool in rental.tools:
            self.inventory.add_tool(tool)
        self.active_rentals.remove(rental)
        self.complete_rentals.append(rental)

    def __str__(self):
        return "Store: \n" \
        + "Inventory: {}\n".format(len(self.inventory.tools)) \
        + "Income: {}\n".format(self.money)

    def __repr__(self):
        return self.__str__()

class Simulation:
    def __init__(self):
        self.days = 0
        self.store = Store()

if __name__ == '__main__':
    pass