import csv
import time
from datetime import datetime
from pymongo import MongoClient

CSV_FILE = "C:/Users/theve/OneDrive/Desktop/cockroach/sales_data.csv"

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["sales"]

collection.delete_many({})
#write
start_write = time.time()
rows_inserted = 0
batch_size = 5000
docs = []

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for idx, row in enumerate(reader, start=1):
        doc = {
            "region": row['Region'],
            "country": row['Country'],
            "item_type": row['Item Type'],
            "sales_channel": row['Sales Channel'],
            "order_priority": row['Order Priority'],
            "order_date": datetime.strptime(row['Order Date'], '%m/%d/%Y'),
            "order_id": int(row['Order ID']),
            "ship_date": datetime.strptime(row['Ship Date'], '%m/%d/%Y'),
            "units_sold": int(row['Units Sold']),
            "unit_price": float(row['Unit Price']),
            "unit_cost": float(row['Unit Cost']),
            "total_revenue": float(row['Total Revenue']),
            "total_cost": float(row['Total Cost']),
            "total_profit": float(row['Total Profit'])
        }
        docs.append(doc)
        if idx % batch_size == 0:
            collection.insert_many(docs)
            rows_inserted += len(docs)
            docs = []

if docs:
    collection.insert_many(docs)
    rows_inserted += len(docs)

elapsed_write = time.time() - start_write
write_latency_ms = (elapsed_write / rows_inserted) * 1000
write_throughput = rows_inserted / elapsed_write

start_read = time.time()
total_rows = collection.count_documents({})
elapsed_read = time.time() - start_read

read_latency_ms = elapsed_read * 1000
read_throughput = total_rows / elapsed_read

aggregations = {}

# max
start_agg = time.time()
collection.aggregate([{ "$group": { "_id": None, "max_units": { "$max": "$units_sold" }}}])
aggregations["MAX"] = (time.time() - start_agg) * 1000

# min
start_agg = time.time()
collection.aggregate([{ "$group": { "_id": None, "min_units": { "$min": "$units_sold" }}}])
aggregations["MIN"] = (time.time() - start_agg) * 1000

# averahge
start_agg = time.time()
collection.aggregate([{ "$group": { "_id": None, "avg_units": { "$avg": "$units_sold" }}}])
aggregations["AVG"] = (time.time() - start_agg) * 1000

client.close()

print(f"Write Latency (ms per insert): {write_latency_ms:.2f}")
print(f"Write Throughput (ops/sec): {write_throughput:.2f}")
print(f"Read Latency (ms): {read_latency_ms:.2f}")
print(f"Read Throughput (ops/sec): {read_throughput:.2f}")

for agg_func, latency in aggregations.items():
    print(f"{agg_func} Aggregation Latency (ms): {latency:.2f}")


