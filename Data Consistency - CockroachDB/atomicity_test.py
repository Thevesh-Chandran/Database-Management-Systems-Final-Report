# atomicity_test.py
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
    conn.autocommit = False
    cur.execute("""
        INSERT INTO sales_data (order_id, item_type, units_sold)
        VALUES (999999, 'AtomicityTest', 100);
    """)
    cur.execute("""
        INSERT INTO sales_data (order_id, item_type, units_sold)
        VALUES (999999, 'AtomicityFail', 50);
    """)
    conn.commit()
except Exception as e:
    print("Transaction failed, rolling back:", e)
    conn.rollback()
finally:
    cur.close()
    conn.close()
