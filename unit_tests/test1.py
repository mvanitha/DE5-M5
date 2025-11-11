import unittest
from calculator_app import Calculator

class TestOperations(unittest.TestCase):

    def test_sum(self):
        calc = Calculator(10,0)
        self.assertEqual(calc.sum(), 10, "Test Fail: Incorrect sum")

    def test_diff(self):
        calc = Calculator(10,0)
        self.assertEqual(calc.diff(), 10, "Test Fail: Incorrect difference")    

    def test_multiply(self):
        calc = Calculator(10,0)
        self.assertEqual(calc.multiply(), 0, "Test Fail: Incorrect multiplication")        

    def test_divide(self):
        calc = Calculator(10,0)
        self.assertEqual(calc.divide(), 0, "Test Fail: Incorrect division") 

if __name__ == "__main__":
    unittest.main()

