Data Upload to MySQL Database from Excel
This script uploads data from an Excel file to a MySQL database, creating tables if they don't exist and inserting data from specified sheets. It’s designed to handle three tables: Orders, Returns, and People.

Prerequisites
Python 3.x
pandas library
mysql-connector-python library
Install necessary Python packages using:

Database Configuration
In the script, update the db_config dictionary with your MySQL database connection details:

python
Copy code
db_config = {
    'host': 'your-db-instance-name',
    'database': 'your_database_name',
    'user': 'your_master_username',
    'password': 'your_master_password',
    'port': 3306
}
Folder Structure
Ensure your Excel file and script are in the same directory, or specify the correct path to the file in the file_path variable.

Instructions
Prepare the Excel File:

Save your Excel file with three sheets: Orders, Returns, and People.
Each sheet should contain data with the columns specified for each table in the script.
Run the Script:

The script will check for the Excel file, create the tables (if they don’t already exist), and upload the data from each sheet to the corresponding table in the database.
Script Details:

create_orders_table(cursor): Creates the Orders table.
create_returns_table(cursor): Creates the Returns table.
create_people_table(cursor): Creates the People table.
upload_table_to_db(df, table_name, cursor): Inserts data from a DataFrame into the specified table.
upload_excel_to_db(file_path, tables_info): Manages database connections, calls table creation functions, and initiates data upload.
Customize the File Path:

Modify the file_path variable with the correct path to your Excel file:
python
Copy code
file_path = "/path/to/your/excel_file.xlsx"
Review the Output:

The script prints log messages indicating the progress of table creation, data upload, and row counts.
Database Connection Closure:

Once all data is uploaded, the database connection will close automatically.
Example Usage
To run this script for the Excel file sample_data.xlsx, update:

python
Copy code
file_path = "/path/to/sample_data.xlsx"
tables_info = {
    "Orders": "Orders",
    "Returns": "Returns",
    "People": "People"
}

