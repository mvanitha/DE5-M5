import unittest
from calculator_app import Calculator

class TestOperations(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator(100,2)
     

    def test_sum(self):
        self.assertEqual(self.calc.sum(), 102, "Fail: Incorrect sum")
             
if __name__ == "__main__":
    unittest.main()

