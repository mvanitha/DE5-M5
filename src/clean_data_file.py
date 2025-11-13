import pandas as pd;
import numpy as np;
import pyodbc;
import argparse;


# Read source data files

in_systembooks_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5\\Data\\03_Library Systembook.csv"
in_systemcustomers_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5\\Data\\03_Library SystemCustomers.csv"

from sqlalchemy import create_engine

# Define the connection string to your MS SQL Server
server = 'localhost'  
database = 'QAAnalysis'

# Create the connection string with Windows Authentication
connection_string = f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

# Create the SQLAlchemy engine
engine = create_engine(connection_string)


def file_checker(filename, filepath):
    print("Reading file {} from location {}".format(filename, filepath))
    try:       
        df_data = pd.read_csv(filepath, delimiter=',')
        return df_data
    except FileNotFoundError:
        print("File not found.")
    except pd.errors.EmptyDataError:
        print("No data")
    except pd.errors.ParserError:
        print("Parse error")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Format headers
def format_df_headers(data):   
    return data.columns.str.replace(' ', '_')

# Remove missing rows
def remove_missing_rows(data):   
    return data.dropna(axis=0)

# Remove duplicates
def remove_duplicates(filesource, data):
        if filesource == "Customer":
            return data.drop_duplicates(subset=['Customer_ID'], keep='last')
        elif filesource == "Book":
            return data.drop_duplicates(subset=['Id'], keep='last')
        else:
            return data.drop_duplicates()
    
def convert_date_datatypes(data):
    #  Convert string to date
    data.loc[:,'Book_checkout'] = data['Book_checkout'].str.replace(r'"', '')
    data.loc[:,'Book_checkout'] = pd.to_datetime(data['Book_checkout'], format='mixed')
    return data

def calculate_borrowing_time(data): 
    #  Convert string to date
    data.loc[:,'Book_checkout'] = data['Book_checkout'].str.replace(r'"', '')
    data.loc[:,'Book_checkout'] = pd.to_datetime(data['Book_checkout'], format='mixed')

    data.loc[:,'Book_Returned'] = data['Book_Returned'].str.replace(r'"', '')
    data.loc[:,'Book_Returned'] = pd.to_datetime(data['Book_Returned'], format='mixed')

    data.loc[:,'Days_Borrowed'] = (data['Book_Returned'] - data['Book_checkout'] ) / np.timedelta64(1, 'D')
    return data    

# Main block                         
if __name__ == "__main__":

    dropCount = 0
    totalCount = 0

    parser = argparse.ArgumentParser()  
    parser.add_argument("--datasource", type=str, help="Input datasource such as Customer, Book, etc")  
    parser.add_argument("--file", type=str, help="Input file path")  
    args = parser.parse_args()
    print(args.file) 
    print(args.datasource) 
    
    
    # Read the file
    df_data = file_checker(args.datasource, args.file)
    
    # Format header columns
    df_data.columns = format_df_headers(df_data)

    print(f"Count of Rows in {args.datasource} file:{len(df_data)}")
    totalCount = len(df_data)

    # Write original data to table
    original_table_name = args.datasource + "Orig"
    df_data.to_sql(original_table_name, con=engine, if_exists='replace', index=False)
    data_log = {
         'LoadName' :  original_table_name
       , 'LoadCount':  totalCount
    }
    df_log = pd.DataFrame([data_log])
    df_log.to_sql('AuditLog', con=engine, if_exists='append', index=False)

    
    # Drop Rows from file with missing data
    df_data = remove_missing_rows(df_data)    
    print(f"Count of Rows in {args.datasource} file after dropping missing rows:{len(df_data)}")

    dl_row = {
         'DataSource' : args.datasource
       , 'DataCheck': "Missing Rows"
       , 'DataCount': (totalCount - len(df_data))
    }
    df_dl = pd.DataFrame([dl_row])
    df_dl.to_sql('DataAnalysis', con=engine, if_exists='append', index=False)


    df_data = remove_duplicates(args.datasource, df_data)
    print(f"Count of Rows in {args.datasource} file after removing duplicates:{len(df_data)}")
   
    dl_row = {
         'DataSource' : args.datasource
       , 'DataCheck': "Duplicates"
       , 'DataCount': (totalCount - len(df_data))
    }
    df_dl = pd.DataFrame([dl_row])
    df_dl.to_sql('DataAnalysis', con=engine, if_exists='append', index=False)
    
    if (args.datasource == 'Book'):       
       try:
            df_data = convert_date_datatypes(df_data)
       except Exception as e:
            df_data.drop(16, inplace=True)
            dropCount += 1
            pass 
       
       df_data = calculate_borrowing_time(df_data) 
      
    # Write transformed data to table
    transformed_table_name = args.datasource + "Transformed"
    df_data.to_sql(transformed_table_name, con=engine, if_exists='replace', index=False)
    data_log = {
         'LoadName' :  transformed_table_name
       , 'LoadCount':  len(df_data)
    }

    df_log = pd.DataFrame([data_log])
    df_log.to_sql('AuditLog', con=engine, if_exists='append', index=False)

# Dispose of the engine
engine.dispose()
