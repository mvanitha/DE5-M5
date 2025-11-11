import pandas as pd;
import numpy as np;
import pyodbc;


# Read source data files

in_systembooks_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Data\\03_Library Systembook.csv"
in_systemcustomers_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Data\\03_Library SystemCustomers.csv"

out_systembooks_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Analysis\\03_Library Systembook.csv"
out_systemcustomers_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Analysis\\03_Library SystemCustomers.csv"

from sqlalchemy import create_engine

# Define the connection string to your MS SQL Server
server = 'localhost'  
database = 'QAETLStagingDB'
username = 'python_app_usr'
password = 'test123'

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
def remove_duplicates(filename, data):
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
    
    # Read the Customers file
    df_customers = file_checker("Customers", in_systemcustomers_file)
    
    # Format header columns
    df_customers.columns = format_df_headers(df_customers)

    #rows_count =  len(df_customers)
    print(f"Count of Rows in Customers file:{len(df_customers)}")

    # Drop Rows from file with missing data
    df_customers = remove_missing_rows(df_customers)    
    print(f"Count of Rows in Customers file after dropping missing rows:{len(df_customers)}")

    df_customers = remove_duplicates("Customers", df_customers)
    print(f"Count of Rows in Customers file after removing duplicates:{len(df_customers)}")
   
    # Read the Books file
    df_books = file_checker("Book", in_systembooks_file)
    
    # Format header columns
    df_books.columns = format_df_headers(df_books)

    # Drop Rows from file with missing data
    print(f"Count of Rows in Books file:{len(df_books)}")
    df_books = remove_missing_rows(df_books)    
    print(f"Count of Rows in Books file after dropping missing rows:{len(df_books)}")
    
    df_books = remove_duplicates("Book", df_books)
    print(f"Count of Rows in Books file after removing duplicates:{len(df_books)}")
    
    try:
        df_books = convert_date_datatypes(df_books)
    except Exception as e:
        df_books.drop(16, inplace=True)
        dropCount += 1
        pass 
        

    df_books = calculate_borrowing_time(df_books)

    # Write the DataFrame to SQL Server

    df_customers.to_sql('Customer', con=engine, if_exists='replace', index=False)
    df_customers_log = {
         'LoadName' : 'Customer'
       , 'LoadCount':  len(df_customers)
    }

    df_log = pd.DataFrame([df_customers_log])
    df_log.to_sql('AuditLog', con=engine, if_exists='append', index=False)

    df_books.to_sql('Book', con=engine, if_exists='replace', index=False)
    df_books_log = {
        'LoadName' : 'Book'
        , 'LoadCount':  len(df_books)

    }
    
    df_log = pd.DataFrame([df_books_log])
    df_log.to_sql('AuditLog', con=engine, if_exists='append', index=False)
