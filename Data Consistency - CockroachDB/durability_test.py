# durability_test.py
import psycopg2

conn = psycopg2.connect(dbname="nordstrom", user="root", host="localhost", port=26257, sslmode="disable")
cur = conn.cursor()

cur.execute("INSERT INTO sales_data (order_id, item_type, units_sold) VALUES (888888, 'DurabilityTest', 50);")
conn.commit()

cur.close()
conn.close()

print("Transaction committed. You can now restart the CockroachDB node and check if it persists.")
