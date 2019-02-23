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
        self.customer = sm.Customer("bob", sm.CustomerType("Casual", 1, 2, 1, 2))

    def test_customer_can_rent(self):
        self.assertEqual(self.customer.can_rent_tools(sm.Store()), False)

class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = sm.Store()
        cat_concrete = sm.ToolCategory("Concrete", 40)
        self.tool_1 = sm.Tool("concrete_tool_1", cat_concrete)
        self.tool_2 = sm.Tool("concrete_tool_2", cat_concrete)
        self.store.inventory.add_tool(self.tool_1)
        self.store.inventory.add_tool(self.tool_2)

    def test_store_rentals(self):
        rental = sm.Rental([self.tool_1], 0, 0)

        self.store.make_rental(rental)
        self.assertEqual(self.store.money, rental.cost())
        self.assertEqual(len(self.store.inventory.tools), 1)

        self.store.return_rental(rental)
        self.assertEqual(len(self.store.inventory.tools), 2)
        self.assertEqual(len(self.store.complete_rentals), 1)
        self.assertEqual(len(self.store.active_rentals), 0)

if __name__ == '__main__':
    unittest.main()