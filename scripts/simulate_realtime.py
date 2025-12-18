import time
import random
from clickhouse_driver import Client
from datetime import datetime
import signal
import sys
import os

# Connect to ClickHouse with credentials
client = Client(
    host='clickhouse',
    port=9000,
    user=os.getenv('CLICKHOUSE_USER', 'default'),
    password=os.getenv('CLICKHOUSE_PASSWORD', ''),
    database='default',
    secure=False
)

# Global flag to control running
RUNNING = True

def signal_handler(sig, frame):
    global RUNNING
    print("Stopping simulator via signal...")
    RUNNING = False

# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def insert_random_data():
    records = []
    for _ in range(5):  # Insert 5 records at a time
        invoice_no = str(random.randint(100000, 999999))
        invoice_date = datetime.now()  # current timestamp
        customer_id = random.randint(1000, 9999)
        stock_code = random.choice(['85123A', '71053', '84406B', '84029G', '84029E'])
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
    FLAG_FILE = "/code/simulator_flag.txt"
    print("Simulator started. Use 'docker exec ... touch /code/simulator_flag.txt' to start, 'rm' to stop.")
    while RUNNING:
        if os.path.exists(FLAG_FILE):
            insert_random_data()
            time.sleep(2)  # Insert every 2 seconds when running
        else:
            print("Simulator paused. Waiting for flag file to resume...")
            time.sleep(1)  # Check every second when paused
    print("Simulator stopped.")