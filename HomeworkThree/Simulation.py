#Gayathri Gude, Michael Yoshimura 
#OODA 4448 Homework Three
#Bruce Montgomery, Spring 2019

from random import randint
import numpy as np 
from abc import ABC, abstractmethod

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
    def __init__(self, tools, start_date, return_date, customer):
        self.tools = tools
        self.return_date = return_date
        self.start_date = start_date 
        self.customer = customer

    def days_rented(self):
        return self.return_date - self.start_date

    def cost(self):
        cost_per_day = sum([tool.category.price for tool in self.tools])
        return self.days_rented() * cost_per_day

    def __str__(self):
        return "Rental Info for {}: {} tools rented from day {} to day {} for ${}".format(self.customer, len(self.tools), self.start_date, self.return_date, self.cost())

    def __repr__(self):
        return self.__str__()

# Responsible for 'going' to the store and either returning or renting tools when it is time
class Customer(ABC):
    def __init__(self, name):
        self.name = name
        self.active_rentals = []
        self.tool_rent_min = 0
        self.tool_rent_max = 0
        self.time_rented_min = 0
        self.time_rented_max = 0

    def get_tools_rented(self):
        return sum([len(rental.tools) for rental in self.active_rentals])

    # If the customer can rent more tools, and if there are tools left to rent from the store
    # NOTE: Having a customer have to know about the store may not be the greatest thing
    def can_rent_tools(self, store):
        return len(store.inventory.tools) >= self.tool_rent_max and self.get_tools_rented() < customer_max_tools

    # The customer is presented the tools from the store, and chooses some to rent randomly
    def rent_tools(self, store, current_date):
        if not self.can_rent_tools(store):
            print("Warning: could not rent tools to customer " + self.name)
        amount = randint(self.tool_rent_min, self.tool_rent_max)
        tools_to_rent = np.random.choice(store.inventory.tools, replace=False, size=amount)
        rent_time = randint(self.time_rented_min, self.time_rented_max)
        rental = Rental(tools_to_rent, current_date, current_date + rent_time, self)
        store.make_rental(rental)
        self.active_rentals.append(rental)

    # The customer returns each tool, and the store is updated as well
    def return_tools(self, store, current_date):
        for rental in self.active_rentals:
            if rental.return_date == current_date:
                store.return_rental(rental)
                self.active_rentals.remove(rental) 

    def update(self, store, current_date): 
        self.return_tools(store, current_date) 
        randomDay = randint(0, 7)
        
        if (randomDay == 0 and self.can_rent_tools(store)):
            self.rent_tools(store, current_date)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

class CustomerCasual(Customer):
    def __init__(self, name):
        super().__init__(name)
        self.tool_rent_min = 1
        self.tool_rent_max = 2
        self.time_rented_min = 1
        self.time_rented_max = 2

class CustomerBusiness(Customer):
    def __init__(self, name):
        super().__init__(name)
        self.tool_rent_min = 3
        self.tool_rent_max = 3
        self.time_rented_min = 7
        self.time_rented_max = 7

class CustomerRegular(Customer):
    def __init__(self, name):
        super().__init__(name)
        self.tool_rent_min = 1
        self.tool_rent_max = 3
        self.time_rented_min = 3
        self.time_rented_max = 5

class Store(ABC):
    def __init__(self):
        self.inventory = Inventory(store_max_tools)
        self.money = 0
        self.complete_rentals = []
        self.active_rentals = []
        self.make_tools()

    @abstractmethod
    def make_tools(self):
        pass

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

class ToolStore(Store):
    def make_tools(self):
        cat_concrete = ToolCategory("Concrete", 40)
        cat_woodwork = ToolCategory("Woodwork", 25) 
        cat_painting = ToolCategory("Painting", 30) 
        cat_plumbing = ToolCategory("Plumbing", 55) 
        cat_yardwork = ToolCategory("Yardwork", 60)

        tool_1 = Tool("concrete_tool_1", cat_concrete)
        tool_2 = Tool("concrete_tool_2", cat_concrete) 
        tool_3 = Tool("concrete_tool_3", cat_concrete)
        tool_4 = Tool("concrete_tool_4", cat_concrete)

        tool_5 = Tool("woodwork_tool_5", cat_woodwork) 
        tool_6 = Tool("woodwork_tool_6", cat_woodwork) 
        tool_7 = Tool("woodwork_tool_7", cat_woodwork) 
        tool_8 = Tool("woodwork_tool_8", cat_woodwork) 
    
        tool_9 = Tool("painting_tool_9", cat_painting)
        tool_10 = Tool("painting_tool_10", cat_painting)
        tool_11 = Tool("painting_tool_11", cat_painting)
        tool_12 = Tool("painting_tool_12", cat_painting)

        tool_13 = Tool("plumbing_tool_13", cat_plumbing)
        tool_14 = Tool("plumbing_tool_14", cat_plumbing)
        tool_15 = Tool("plumbing_tool_15", cat_plumbing)
        tool_16 = Tool("plumbing_tool_16", cat_plumbing)

        tool_17 = Tool("yardwork_tool_17", cat_yardwork)
        tool_18 = Tool("yardwork_tool_18", cat_yardwork)
        tool_19 = Tool("yardwork_tool_19", cat_yardwork)
        tool_20 = Tool("yardwork_tool_20", cat_yardwork)

        self.inventory.add_tool(tool_1)
        self.inventory.add_tool(tool_2)
        self.inventory.add_tool(tool_3)
        self.inventory.add_tool(tool_4)
        self.inventory.add_tool(tool_5)
        self.inventory.add_tool(tool_6)
        self.inventory.add_tool(tool_7)
        self.inventory.add_tool(tool_8)
        self.inventory.add_tool(tool_9)
        self.inventory.add_tool(tool_10)
        self.inventory.add_tool(tool_11)
        self.inventory.add_tool(tool_12)
        self.inventory.add_tool(tool_13)
        self.inventory.add_tool(tool_14)
        self.inventory.add_tool(tool_15)
        self.inventory.add_tool(tool_16)
        self.inventory.add_tool(tool_17)
        self.inventory.add_tool(tool_18)
        self.inventory.add_tool(tool_19)
        self.inventory.add_tool(tool_20)

class Simulation:

    def __init__(self):
        self.days = 0 

    def createCustomer(self):
        customer1 = CustomerCasual("Casual: customer1")
        customer2 = CustomerCasual("Casual: customer2")
        customer3 = CustomerCasual("Casual: customer3")
        customer4 = CustomerRegular("Regular: customer4")
        customer5 = CustomerRegular("Regular: customer5")
        customer6 = CustomerRegular("Regular: customer6")
        customer7 = CustomerBusiness("Business: customer7")
        customer8 = CustomerBusiness("Business: ustomer8")
        customer9 = CustomerBusiness("Business: customer9")
        customer10 = CustomerBusiness("Business: customer10")  

        customersList = [customer1, customer2, customer3, customer4, customer5, customer6, customer7, customer8, customer9, customer10]

        return customersList


    def simulationMain(self): 
        # Setup the objects
        store = ToolStore() 
        customerList = self.createCustomer()
        
        #def __init__(self, type_name, tool_rent_min, tool_rent_max, time_rented_min, time_rented_max):
        #print("Initial {}".format(store))

        # Simulate 35 days

        for current_date in range(35): 
            for customer in customerList: 
                customer.update(store, current_date)

        print("Final {}".format(store))

        print("Completed Rentals: ")
        for rental in store.complete_rentals:
            print(rental)

        print("Active Rentals: ")
        for rental in store.active_rentals:
            print(rental) 

        #return(10)

if __name__ == '__main__':
    SimulationMain2 = Simulation()
    SimulationMain2.simulationMain()