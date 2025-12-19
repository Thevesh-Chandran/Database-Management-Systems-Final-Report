# consistency_test.py
import psycopg2

conn = psycopg2.connect(
    dbname="nordstrom",
    user="root",
    host="localhost",
    port=26257,
    sslmode="disable"
)
cur = conn.cursor()

try:
    # This should fail if order_id is primary key
    cur.execute("INSERT INTO sales_data (order_id, item_type) VALUES (1, 'ConsistencyTest');")
    conn.commit()
except Exception as e:
    print("Consistency check caught an error:", e)
finally:
    cur.close()
    conn.close()
