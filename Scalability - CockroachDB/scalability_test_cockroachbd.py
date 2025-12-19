import csv
import psycopg2
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

CSV_FILE = "C:/Users/theve/OneDrive/Desktop/cockroach/sales_data.csv"
BATCH_SIZE = 5000

nodes_sets = [
    [{"name": "Node 1", "host": "localhost", "port": 26257}],
    [{"name": "Node 1", "host": "localhost", "port": 26257},
     {"name": "Node 2", "host": "localhost", "port": 26258}],
    [{"name": "Node 1", "host": "localhost", "port": 26257},
     {"name": "Node 2", "host": "localhost", "port": 26258},
     {"name": "Node 3", "host": "localhost", "port": 26259}]
]

def chunked(iterable, size):
    """Yield successive chunks of a given size."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def import_data(node):
    conn = psycopg2.connect(
        dbname="nordstrom",
        user="root",
        host=node['host'],
        port=node['port'],
        sslmode="disable"
    )
    cur = conn.cursor()

    # Load CSV into memory
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))

    start_time = time.time()
    rows_inserted = 0

    for batch in chunked(reader, BATCH_SIZE):
        values = []
        for row in batch:
            values.append((
                row['Region'], row['Country'], row['Item Type'], row['Sales Channel'],
                row['Order Priority'], datetime.strptime(row['Order Date'], '%m/%d/%Y'),
                int(row['Order ID']), datetime.strptime(row['Ship Date'], '%m/%d/%Y'),
                int(row['Units Sold']), float(row['Unit Price']), float(row['Unit Cost']),
                float(row['Total Revenue']), float(row['Total Cost']), float(row['Total Profit'])
            ))

        # Build SQL for the whole batch
        args_str = ",".join(
            cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8')
            for x in values
        )
        sql = f"""
        INSERT INTO sales_data (
            region, country, item_type, sales_channel, order_priority,
            order_date, order_id, ship_date, units_sold, unit_price,
            unit_cost, total_revenue, total_cost, total_profit
        ) VALUES {args_str}
        ON CONFLICT (order_id) DO UPDATE SET item_type = EXCLUDED.item_type
        """

        # Execute batch insert
        cur.execute(sql)
        conn.commit()
        rows_inserted += len(batch)

    elapsed = time.time() - start_time
    write_throughput = rows_inserted / elapsed if elapsed > 0 else 0

    # Measure read throughput
    read_start = time.time()
    cur.execute("SELECT COUNT(*) FROM sales_data;")
    total_rows = cur.fetchone()[0]
    read_elapsed = time.time() - read_start
    read_throughput = total_rows / read_elapsed if read_elapsed > 0 else 0

    cur.close()
    conn.close()
    return node['name'], write_throughput, read_throughput


for i, nodes in enumerate(nodes_sets, start=1):
    print(f"\n=== Testing with {i} node(s) ===")

    # Clear table before each test
    conn = psycopg2.connect(dbname="nordstrom", user="root", host="localhost", 
    port=26257, sslmode="disable")
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE sales_data;")
    conn.commit()
    cur.close()
    conn.close()

    results = []
    with ThreadPoolExecutor(max_workers=len(nodes)) as executor:
        futures = [executor.submit(import_data, node) for node in nodes]
        for future in futures:
            results.append(future.result())

    base_write = results[0][1] if results[0][1] > 0 else 1
    base_read = results[0][2] if results[0][2] > 0 else 1
    print("| Node | Write Throughput (ops/sec) | Read Throughput (ops/sec) | Write Scale | Read Scale |")
    print("|------|----------------------------|---------------------------|-------------|------------|")
    for node_name, wthr, rthr in results:
        print(f"| {node_name} | {wthr:.2f} | {rthr:.2f} | {wthr/base_write:.2f}× | {rthr/base_read:.2f}× |")
