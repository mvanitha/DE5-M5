import pandas as pd;
import numpy as np;

# Read source data files

in_systembooks_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Data\\03_Library Systembook.csv"
in_systemcustomers_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Data\\03_Library SystemCustomers.csv"

out_systembooks_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Analysis\\03_Library Systembook.csv"
out_systemcustomers_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Analysis\\03_Library SystemCustomers.csv"


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
    print(f"Filename: {filename}")  
    if filename == 'Customers':      
        return data.Customer_ID.unique()
    elif filename == 'Book':
        return data.Id.unique()
    else:
        print(f"Not a valid data file")
        return data
    
def calculate_borrowing_time(data): 
    try:
        #  Convert string to date
        data.loc[:,'Book_checkout'] = data['Book_checkout'].str.replace(r'"', '')
        data.loc[:,'Book_checkout'] = pd.to_datetime(data['Book_checkout'], format='mixed')
        #data.head()
        #data.info()
    except Exception as e:
        print(f"Error occurred: {e}")    


# Main block                         
if __name__ == "__main__":
    
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

    df_books = calculate_borrowing_time(df_books)
    print(df_books)




