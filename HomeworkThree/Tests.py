import unittest
from Simulation import ToolCategory, Tool

class TestTools(unittest.TestCase):
    def setUp(self):
        self.cat_concrete = ToolCategory("Concrete", 40)

    def test_to_string(self):
        tool1 = Tool("tool1", self.cat_concrete)
        self.assertEqual(str(tool1), "tool1")
        self.assertEqual(str(tool1.category), "Concrete")

if __name__ == '__main__':
    unittest.main()