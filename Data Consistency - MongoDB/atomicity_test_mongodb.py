from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Connect to MongoDB replica set
client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
db = client["mydb"]
collection = db["sales"]

# Ensure unique index on order_id
collection.create_index("order_id", unique=True)

# Start a session for transaction
with client.start_session() as session:
    try:
        with session.start_transaction():
            collection.insert_one(
                {"order_id": 999999, "item_type": "AtomicityTest", "units_sold": 100},
                session=session
            )

            # Force an error (duplicate primary key)
            collection.insert_one(
                {"order_id": 999999, "item_type": "AtomicityFail", "units_sold": 50},
                session=session
            )

        print("Transaction committed successfully (should not happen)")
    except DuplicateKeyError as e:
        print("Transaction failed and rolled back due to duplicate key:", e)
    except Exception as e:
        print("Transaction failed and rolled back:", e)

count = collection.count_documents({"order_id": 999999})
print(f"Number of documents with order_id 999999: {count}")
