import pandas as pd;

# Read source data files

in_systembooks_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Data\\03_Library Systembook.csv"
in_systemcustomers_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Data\\03_Library SystemCustomers.csv"

out_systembooks_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Analysis\\03_Library Systembook.csv"
out_systemcustomers_file = "C:\\Users\\Admin\\Desktop\\DE_M5\\gitrepos\\DE5-M5-20251110\\Analysis\\03_Library SystemCustomers.csv"

df_books = pd.read_csv(in_systembooks_file, delimiter=',')
df_customers = pd.read_csv(in_systemcustomers_file, delimiter=',')

# Drop Rows from Books file with missing data
cl_dfbooks = df_books.dropna(axis=0)

# Remove duplicates
cl_dfbooks.Id.unique()
#print(cl_dfbooks)

#  Convert string to date
cl_dfbooks['Book checkout'] = cl_dfbooks['Book checkout'].str.replace(r'"', '')
pd.to_datetime(cl_dfbooks['Book checkout'], format="%d/%m/%Y", errors='coerce')

# Drop Rows from Books file with missing data
cl_df_customers = df_customers.dropna(axis=0)

#Write data frames to the output folder
cl_dfbooks.to_csv(out_systembooks_file);
cl_df_customers.to_csv(out_systemcustomers_file);
                