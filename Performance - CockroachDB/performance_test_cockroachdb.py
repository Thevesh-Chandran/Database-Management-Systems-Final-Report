import csv
import psycopg2
import psycopg2.extras
import time
from datetime import datetime

CSV_FILE = "C:/Users/theve/OneDrive/Desktop/cockroach/sales_data.csv"
BATCH_SIZE = 5000
MAX_RETRIES = 5

def chunked(iterable, size):
    """Yield successive chunks of a given size."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]
# Load CSV into memory
with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = list(csv.DictReader(csvfile))

conn = psycopg2.connect(
    dbname="nordstrom",user="root",host="localhost",port=26257,
    sslmode="disable"
)
cur = conn.cursor()
# Clear table
cur.execute("TRUNCATE TABLE sales_data;")
conn.commit()

start_write = time.time()
insert_query = """
    INSERT INTO sales_data (region, country, item_type, sales_channel,
    order_priority,order_date, order_id, ship_date, units_sold, 
    unit_price,unit_cost, total_revenue, total_cost, total_profit
    ) VALUES %s
    ON CONFLICT (order_id)
    DO UPDATE SET item_type = EXCLUDED.item_type;
"""

for batch in chunked(reader, BATCH_SIZE):
    values = [
        (
            row['Region'],row['Country'],row['Item Type'],row['Sales Channel'],
            row['Order Priority'],datetime.strptime(row['Order Date'], 
            '%m/%d/%Y'),int(row['Order ID']),
            datetime.strptime(row['Ship Date'], '%m/%d/%Y'),
            int(row['Units Sold']),float(row['Unit Price']),
            float(row['Unit Cost']),float(row['Total Revenue']),
            float(row['Total Cost']),float(row['Total Profit'])
        )
        for row in batch
    ]
    for attempt in range(MAX_RETRIES):
        try:
            psycopg2.extras.execute_values(
                cur,
                insert_query,
                values,
                page_size=BATCH_SIZE
            )
            conn.commit()
            break
        except psycopg2.errors.SerializationFailure:
            conn.rollback()
            print(f"Batch retry ({attempt + 1}/{MAX_RETRIES})...")
            time.sleep(0.5)

cur.execute("SELECT COUNT(*) FROM sales_data;")
rows_inserted = cur.fetchone()[0]
elapsed_write = time.time() - start_write

write_latency_ms = (elapsed_write / rows_inserted) * 1000
write_throughput = rows_inserted / elapsed_write

# Read performance
start_read = time.time()
cur.execute("SELECT COUNT(*) FROM sales_data;")
total_rows = cur.fetchone()[0]
elapsed_read = time.time() - start_read

read_latency_ms = elapsed_read * 1000
read_throughput = total_rows / elapsed_read

# Aggregations
aggregations = {}
for agg_func in ['MAX', 'MIN', 'AVG']:
    start_agg = time.time()
    cur.execute(f"SELECT {agg_func}(units_sold) FROM sales_data;")
    _ = cur.fetchone()[0]
    elapsed_agg = time.time() - start_agg
    aggregations[agg_func] = elapsed_agg * 1000
cur.close()
conn.close()

# Print results
print(f"Write Latency (ms per insert): {write_latency_ms:.2f}")
print(f"Write Throughput (ops/sec): {write_throughput:.2f}")
print(f"Read Latency (ms): {read_latency_ms:.2f}")
print(f"Read Throughput (ops/sec): {read_throughput:.2f}")
for agg_func, latency in aggregations.items():
    print(f"{agg_func} Aggregation Latency (ms): {latency:.2f}")
