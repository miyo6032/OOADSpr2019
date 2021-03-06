import unittest
import Simulation as sm

class TestTools(unittest.TestCase):
    def setUp(self):
        self.cat_concrete = sm.ToolCategory("Concrete", 40)

    def test_to_string(self):
        tool1 = sm.Tool("tool1", self.cat_concrete)
        self.assertEqual(str(tool1), "tool1")
        self.assertEqual(str(tool1.category), "Concrete")

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = sm.Inventory(3)
        self.cat_concrete = sm.ToolCategory("Concrete", 40)
        self.tool = sm.Tool("tool1", self.cat_concrete)

    def test_inventory_add_remove(self):
        self.assertEqual(self.inventory.empty(), True)
        self.inventory.add_tool(self.tool)
        self.assertEqual(self.inventory.empty(), False)
        self.inventory.remove_tool(self.tool)
        self.assertEqual(self.inventory.empty(), True)

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.customer = sm.CustomerCasual("bob")

    def test_customer_can_rent(self):
        self.assertEqual(self.customer.can_rent_tools(sm.ToolStore()), True)

if __name__ == '__main__':
    unittest.main()