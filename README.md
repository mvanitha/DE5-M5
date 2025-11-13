# DE5-M5
Data Engineering Module 5

Author: Vanitha Mascarenhas


Created a python file 'clean_data_file.py' that accepts these 3 parameters
DataSource for e.g. Customer , Book
FilePath where the file resides

The python file performs the following tasks

- Reads the file
- Identifies and drops the missing rows(NaN)
- Identifies and drops the duplicate rows
- Logs the count of anomalies in the dbo.DataAnalysis table
- Calculates the 'Days borrowed' metric
- Loads the original data read from the file in the dbo.<DataSource>Orig table
- Loads the transformed data read from the file in the dbo.<DataSource>Transformed table

Created a dashboard in Power BI reporting these metrics
-- Number of Delayed Borrowers
-- Anomalies per Data Source
-- 





