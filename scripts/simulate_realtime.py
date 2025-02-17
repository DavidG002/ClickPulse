import time
import random
from clickhouse_driver import Client
from datetime import datetime

# Connect to ClickHouse
client = Client(host='clickhouse', port=9000)

def insert_random_data():
    records = []
    for _ in range(5):  # Insert 5 records at a time
        invoice_no = str(random.randint(100000, 999999))
        invoice_date = datetime.now()  # current timestamp
        customer_id = random.randint(1000, 9999)
        stock_code = random.choice(['85123A', '71053', '84406B', '84029G', '84029E'])
        # Increase the range for quantity and unit price
        quantity = random.randint(5, 20)
        unit_price = round(random.uniform(10.0, 50.0), 2)
        sales_amount = quantity * unit_price
        country = random.choice(['United Kingdom', 'France', 'Australia', 'Netherlands'])
        
        records.append((
            invoice_no, invoice_date, customer_id,
            stock_code, quantity, unit_price,
            sales_amount, country
        ))
    
    insert_query = """
    INSERT INTO online_retail 
    (InvoiceNo, InvoiceDate, CustomerID, StockCode, Quantity, UnitPrice, SalesAmount, Country)
    VALUES
    """
    client.execute(insert_query, records)
    print(f"Inserted {len(records)} records.")

if __name__ == '__main__':
    while True:
        insert_random_data()
        # Insert every 2 seconds for more rapid changes
        time.sleep(2)
