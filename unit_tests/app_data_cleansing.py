from datetime import datetime, date
import pandas as pd
import numpy as np

class DataCleansing:

    def xxx__init__(self, from_date: str, to_date: str):
        self.date_from = datetime.strptime(to_date, "%Y-%m-%d").date() 
        self.date_to = datetime.strptime(from_date, "%Y-%m-%d").date()

    # Accepts data frame as parameter
    def __init__(self, df_in):
        self.data = df_in
    
    def calculate_borrowing_time(self): 
        self.data.loc[:,'Book_checkout'] = self.data['Book_checkout'].str.replace(r'"', '')
        self.data.loc[:,'Book_checkout'] = pd.to_datetime(self.data['Book_checkout'], format='mixed')

        self.inputdata_df.loc[:,'Book_Returned'] = self.data['Book_Returned'].str.replace(r'"', '')
        self.data.loc[:,'Book_Returned'] = pd.to_datetime(self.data['Book_Returned'], format='mixed')

        self.data.loc[:,'Days_Borrowed'] = (self.data['Book_Returned'] - self.data['Book_checkout'] ) / np.timedelta64(1, 'D')
        return self.data
  

'''
data = {
    "Book_checkout": ["2025-11-01"],
    "Book_Returned": ["2025-11-12"]
}

df = DataCleansing(pd.DataFrame(data))
result = df.calculate_borrowing_time()
print(result['Days_Borrowed'].loc[result.index[0]])


borrowTime = DataCleansing("2025-11-01", "2025-11-12")
print(borrowTime.calculate_borrowing_time())
'''
