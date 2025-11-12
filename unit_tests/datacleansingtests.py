import unittest
import pandas as pd

from app_data_cleansing import DataCleansing

class TestOperations(unittest.TestCase):

    def xxxtest_borrow_time(self):
        input = DataCleansing("2025-11-01", "2025-11-12")
        self.assertEqual(input.calculate_borrowing_time(), 11, "Test Fail: Incorrect number of days")

    def setUp(self):
        df = {
                "Book_checkout": ["2025-11-01"],
                "Book_Returned": ["2025-11-12"]
             }    
        self.input_df = DataCleansing(pd.DataFrame(df))

    def test_borrow_time(self):        
        result = self.input_df.calculate_borrowing_time()
        self.assertEqual(result['Days_Borrowed'].loc[result.index[0]], 11, "Test Fail: Incorrect number of days")    

if __name__ == "__main__":
    unittest.main()

