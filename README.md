# Birds Analysis

TensorFlow analysis with data from Cornell's eBird database

Accessed csv file of eBird Observation Dataset from Cornell Lab of Ornithology
on Global Biodiversity Information Facility (GBIF) website:
https://www.gbif.org/dataset/4fa7b334-ce0d-4e88-aaae-2e0c138d049e

Shortened data to more manageable chunk with **GetShortCSV.py**

Wrote python code to create SQL queries in order to transfer data from
csv file to SQL database with **CSVtoSQLqueries.py**
- Output txt files with query commands stored **python_output_txt_files** folder
- Actual SQL query files in **SQL_queries** folder
  - Creating all tables (this was written by hand to create schema and tables
  - All other files are the queries to insert data into tables


Example query of data stored in main table:
![](https://github.com/savanaconda/Birds-Analysis/blob/master/Images/SQL%20table%20example.png)

SQL database structure outlined in **Birds_SQL_databasestructure.pdf**
