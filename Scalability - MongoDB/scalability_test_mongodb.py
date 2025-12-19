import csv
import time
from datetime import datetime
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

CSV_FILE = "C:/Users/theve/OneDrive/Desktop/cockroach/sales_data.csv"

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["sales"]

# load CSV into memory
docs = []
with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        docs.append({
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
        })

nodes_sets = [1, 2, 3]
BATCH_SIZE = 5000

def insert_batch(batch):
    start_time = time.time()
    collection.insert_many(batch)
    elapsed = time.time() - start_time
    throughput = len(batch) / elapsed if elapsed > 0 else 0
    return throughput

for num_nodes in nodes_sets:
    print(f"\n=== Testing with {num_nodes} node(s) ===")
    collection.delete_many({})
    # Split into batches of 5k for each node
    batches = [docs[i:i + BATCH_SIZE] for i in range(0, len(docs), BATCH_SIZE)]

    # Distribute batches evenly among threads
    thread_batches = [[] for _ in range(num_nodes)]
    for i, batch in enumerate(batches):
        thread_batches[i % num_nodes].extend(batch)

    results = []
    with ThreadPoolExecutor(max_workers=num_nodes) as executor:
        results = list(executor.map(insert_batch, thread_batches))
    read_start = time.time()
    total_rows = collection.count_documents({})
    read_elapsed = time.time() - read_start
    read_throughput = total_rows / read_elapsed if read_elapsed > 0 else 0
    base_write = results[0] if results[0] > 0 else 1
    base_read = read_throughput if read_throughput > 0 else 1

    print("| Node | Write Throughput (ops/sec) | Read Throughput (ops/sec) | Write Scale | Read Scale |")
    print("|------|----------------------------|---------------------------|-------------|------------|")
    for i, wthr in enumerate(results, start=1):
        print(f"|Node {i} |{wthr:.2f} |{read_throughput:.2f} |{wthr/base_write:.2f}× |{read_throughput/base_read:.2f}× |")
