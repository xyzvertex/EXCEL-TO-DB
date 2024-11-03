import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

# Database connection parameters
db_config = {
    db_config = {
    'host': 'your-db-instance-name.',
    'database': 'your_database_name',
    'user': 'your_master_username',
    'password': 'your_master_password',
    'port': 3306
}
def create_orders_table(cursor):
    sql = """
    CREATE TABLE IF NOT EXISTS Orders (
        `Row ID` INT PRIMARY KEY,
        `OrderID` VARCHAR(20) NOT NULL,
        `OrderDate` DATE NOT NULL,
        `ShipDate` DATE,
        `ShipMode` VARCHAR(50),
        `CustomerID` VARCHAR(20) NOT NULL,
        `CustomerName` VARCHAR(255) NOT NULL,
        `Segment` VARCHAR(50),
        `Country` VARCHAR(100),
        `City` VARCHAR(100),
        `State` VARCHAR(100),
        `PostalCode` VARCHAR(20),
        `Region` VARCHAR(100),
        `ProductID` VARCHAR(20) NOT NULL,
        `Category` VARCHAR(50),
        `SubCategory` VARCHAR(50),
        `ProductName` VARCHAR(255),
        `Sales` DECIMAL(10, 2),
        `Quantity` INT,
        `Discount` DECIMAL(5, 2),
        `Profit` DECIMAL(10, 2)
    );
    """
    cursor.execute(sql)
    print("Table 'Orders created or already exists.")

def create_returns_table(cursor):
    sql = """
    CREATE TABLE IF NOT EXISTS Returns (
        `Returned` VARCHAR(3),
        `OrderID` VARCHAR(20) NOT NULL
    );
    """
    cursor.execute(sql)
    print("Table 'Returns' created or already exists.")

def create_people_table(cursor):
    sql = """
    CREATE TABLE IF NOT EXISTS People (
        `Person` VARCHAR(255) NOT NULL,
        `Region` VARCHAR(100)
    );
    """
    cursor.execute(sql)
    print("Table 'Orders' created or already exists.")

def upload_table_to_db(df, table_name, cursor):
    for index, row in df.iterrows():
        print(f"Inserting row: {row}")  # Debugging: print the row being inserted

        if table_name == "Orders":
            sql = f"""
            INSERT INTO `{table_name}` (
                `Row ID`, `OrderID`, `OrderDate`, `ShipDate`, `ShipMode`, 
                `CustomerID`, `CustomerName`, `Segment`, `Country`, `City`, 
                `State`, `PostalCode`, `Region`, `ProductID`, `Category`, 
                `SubCategory`, `ProductName`, `Sales`, `Quantity`, `Discount`, 
                `Profit`
            ) VALUES (
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s
            )
            """
            cursor.execute(sql, (
                row['Row ID'], row['Order ID'], row['Order Date'], row['Ship Date'], row['Ship Mode'],
                row['Customer ID'], row['Customer Name'], row['Segment'], row['Country'], row['City'],
                row['State'], row['Postal Code'], row['Region'], row['Product ID'], row['Category'],
                row['Sub-Category'], row['Product Name'], row['Sales'], row['Quantity'], row['Discount'],
                row['Profit']
            ))
        elif table_name == "Returns":
            sql = f"""
            INSERT INTO `{table_name}` (
                `Returned`, `OrderID`
            ) VALUES (
                %s, %s
            )
            """
            cursor.execute(sql, (row['Returned'], row['Order ID']))
        elif table_name == "People":
            sql = f"""
            INSERT INTO `{table_name}` (
                `Person`, `Region`
            ) VALUES (
                %s, %s
            )
            """
            cursor.execute(sql, (row['Person'], row['Region']))

def upload_excel_to_db(file_path, tables_info):
    connection = None
    try:
        print(f"Checking file at: {file_path}")
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return

        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            cursor = connection.cursor()

            for table_name, sheet_name in tables_info.items():
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                print("DataFrame Columns:", df.columns)
                print("Number of Columns in DataFrame:", len(df.columns))

                if table_name == "Orders":
                    create_orders_table(cursor)
                elif table_name == "Returns":
                    create_returns_table(cursor)
                elif table_name == "People":
                    create_people_table(cursor)

                upload_table_to_db(df, table_name, cursor)

                connection.commit()
                print(f"Data uploaded successfully to '{table_name}'.")

                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`;")
                row_count = cursor.fetchone()[0]
                print(f"Number of rows in '{table_name}': {row_count}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

# Define the file path and the mapping of table names to Excel sheet names
file_path = "home/xx/xx."  # Adjust the path as needed
tables_info = {
    "Orders":  "Orders",              # Table name: Excel sheet name
    "Returns": "Returns",            # Table name: Excel sheet name for Returns
    "People": "People"               # Table name: Excel sheet name for People
}

# Call the function to upload data
upload_excel_to_db(file_path, tables_info)