from pymongo import MongoClient
from pymongo.errors import OperationFailure, PyMongoError
import threading
import time
import datetime

client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
db = client.mydb
collection = db.sales

#reset test document
collection.update_one(
    {"order_id": 1},
    {"$set": {"item_type": "IsolationTest", "units_sold": 0}},
    upsert=True
)
def transaction_with_logging(name, increment, pause=False, max_retries=10):
    retry_count = 0
    with client.start_session() as session:
        while True:
            try:
                with session.start_transaction():
                    doc = collection.find_one({"order_id": 1}, session=session)
                    print(f"{name}: read units_sold = {doc['units_sold']} at {datetime.datetime.now()}")
                    collection.update_one(
                        {"order_id": 1},
                        {"$inc": {"units_sold": increment}},
                        session=session
                    )
                    print(f"{name}: incremented by {increment} at {datetime.datetime.now()}")
                    if pause:
                        input(f"{name}: paused mid-transaction. Press Enter to continue...")
                print(f"{name}: committed at {datetime.datetime.now()}\n")
                break 
            except OperationFailure as e:
                labels = getattr(e, 'details', {}).get('errorLabels', [])
                if 'TransientTransactionError' in labels:
                    retry_count += 1
                    if retry_count <= max_retries:
                        print(f"{name}: transient error, retrying... attempt {retry_count}")
                    time.sleep(1) 
                    continue
                else:
                    print(f"{name}: transaction failed: {e}")
                    break
            except PyMongoError as e:
                print(f"{name}: transaction failed: {e}")
                break
t1 = threading.Thread(target=lambda: transaction_with_logging("T1", 10, pause=True))
t2 = threading.Thread(target=lambda: transaction_with_logging("T2", 5))
t1.start()
time.sleep(0.2)
t2.start()
t1.join()
t2.join()

final_doc = collection.find_one({"order_id": 1})
print("Final document:", final_doc)
