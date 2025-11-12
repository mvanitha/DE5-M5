# test_reversal.py
import pytest
import pandas as pd
from app_data_cleansing import DataCleansing

def reverse_text(text):
    return text[::-1]

def test_reverse_text():
    assert reverse_text('python') == 'nohtyp'

def test_borrow_time():  
    df = {
                "Book_checkout": ["2025-11-01"],
                "Book_Returned": ["2025-11-12"]
         }    
    input_df = DataCleansing(pd.DataFrame(df))      
    result = input_df.calculate_borrowing_time()
    assert result['Days_Borrowed'].loc[result.index[0]] == 11