# isolation_test.py
import psycopg2
import threading

def transaction1():
    conn = psycopg2.connect(dbname="nordstrom", user="root", host="localhost", port=26257, sslmode="disable")
    cur = conn.cursor()
    conn.autocommit = False
    cur.execute("UPDATE sales_data SET units_sold = units_sold + 10 WHERE order_id = 1;")
    input("Transaction 1 paused, press Enter to continue...")
    conn.commit()
    cur.close()
    conn.close()

def transaction2():
    conn = psycopg2.connect(dbname="nordstrom", user="root", host="localhost", port=26257, sslmode="disable")
    cur = conn.cursor()
    conn.autocommit = False
    cur.execute("UPDATE sales_data SET units_sold = units_sold + 5 WHERE order_id = 1;")
    conn.commit()
    cur.close()
    conn.close()

t1 = threading.Thread(target=transaction1)
t2 = threading.Thread(target=transaction2)

t1.start()
t2.start()
t1.join()
t2.join()
