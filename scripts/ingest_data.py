import csv
from clickhouse_driver import Client
from datetime import datetime
import time

def connect_with_retry(host='clickhouse', port=9000, retries=5, delay=5):
    for attempt in range(retries):
        try:
            client = Client(host=host, port=port)
            client.execute("SELECT 1")  # Test connection
            return client
        except Exception as e:
            print(f"Attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise Exception("Failed to connect to ClickHouse after retries")

# Connect to ClickHouse with retry
client = connect_with_retry(host='clickhouse', port=9000)

# Create table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS online_retail (
    InvoiceNo String,
    InvoiceDate DateTime,
    CustomerID UInt64,
    StockCode String,
    Quantity Int32,
    UnitPrice Float64,
    SalesAmount Float64,
    Country String
) ENGINE = MergeTree()
ORDER BY InvoiceDate
"""
client.execute(create_table_query)
print("Table 'online_retail' is ready.")

# Path to your CSV file
csv_file = "CSV-files/data.csv"

rows = []
max_rows = 50000  # Limit to first 50,000 rows for testing

with open(csv_file, newline='', encoding='windows-1252') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i >= max_rows:
            break
        try:
            invoice_no = row['InvoiceNo']
            invoice_date = datetime.strptime(row['InvoiceDate'], "%m/%d/%Y %H:%M")
            if row['CustomerID'] == "":
                continue
            customer_id = int(float(row['CustomerID']))
            stock_code = row['StockCode']
            quantity = int(row['Quantity'])
            unit_price = float(row['UnitPrice'])
            sales_amount = quantity * unit_price
            country = row['Country']
            rows.append((
                invoice_no, invoice_date, customer_id,
                stock_code, quantity, unit_price,
                sales_amount, country
            ))
        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

# Insert rows into ClickHouse
insert_query = """
INSERT INTO online_retail 
(InvoiceNo, InvoiceDate, CustomerID, StockCode, Quantity, UnitPrice, SalesAmount, Country)
VALUES
"""
client.execute(insert_query, rows)
print("Data ingestion complete for first", len(rows), "rows!")