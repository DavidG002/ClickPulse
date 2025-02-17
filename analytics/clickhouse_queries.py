# C:\Users\David\Apps-Start\Start-ClickPulse\analytics\clickhouse_queries.py

import time
from clickhouse_driver import Client

def get_total_sales_per_day():
    client = Client(host='clickhouse', port=9000)
    query = """
    SELECT toDate(InvoiceDate) AS sale_date, sum(Quantity * UnitPrice) AS total_sales
    FROM online_retail
    GROUP BY sale_date
    ORDER BY sale_date;
    """
    result = client.execute(query)
    # Format each row as a dictionary
    return [{"sale_date": sale_date.isoformat(), "total_sales": total_sales} for sale_date, total_sales in result]

def get_total_sales_by_country():
    client = Client(host='clickhouse', port=9000)
    query = """
    SELECT Country, sum(Quantity * UnitPrice) AS total_sales
    FROM online_retail
    GROUP BY Country
    ORDER BY total_sales DESC;
    """
    result = client.execute(query)
    return [{"Country": country, "total_sales": total_sales} for country, total_sales in result]

def get_average_order_value():
    client = Client(host='clickhouse', port=9000)
    query = """
    SELECT avg(order_total) FROM (
      SELECT InvoiceNo, sum(Quantity * UnitPrice) AS order_total
      FROM online_retail
      GROUP BY InvoiceNo
    )
    """
    result = client.execute(query)
    avg_value = result[0][0] if result else None
    return avg_value

def measure_total_sales_query_time():
    client = Client(host='clickhouse', port=9000)
    query = "SELECT sum(Quantity * UnitPrice) FROM online_retail"
    
    start = time.time()
    client.execute(query)
    end = time.time()
    
    # Calculate execution time in milliseconds
    execution_time_ms = (end - start) * 1000
    return execution_time_ms
