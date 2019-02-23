import unittest
from Simulation import ToolCategory, Tool, Inventory, Customer, CustomerType, Store

class TestTools(unittest.TestCase):
    def setUp(self):
        self.cat_concrete = ToolCategory("Concrete", 40)

    def test_to_string(self):
        tool1 = Tool("tool1", self.cat_concrete)
        self.assertEqual(str(tool1), "tool1")
        self.assertEqual(str(tool1.category), "Concrete")

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory(3)
        self.cat_concrete = ToolCategory("Concrete", 40)
        self.tool = Tool("tool1", self.cat_concrete)

    def test_inventory_add_remove(self):
        self.assertEqual(self.inventory.empty(), True)
        self.inventory.add_tool(self.tool)
        self.assertEqual(self.inventory.empty(), False)
        self.inventory.remove_tool(self.tool)
        self.assertEqual(self.inventory.empty(), True)

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("bob", CustomerType("Casual", 1, 2, 1, 2))

    def test_customer_can_rent(self):
        self.assertEqual(self.customer.can_rent_tools(Store()), False)

if __name__ == '__main__':
    unittest.main()