from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Connect to the MongoDB replica set
client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
db = client.mydb
collection = db.sales

with client.start_session() as session:
    try:
        with session.start_transaction():
            # Try inserting a duplicate order_id
            collection.insert_one({"order_id": 1, "item_type": "ConsistencyTest"}, session=session)
            collection.insert_one({"order_id": 1, "item_type": "ConsistencyTest2"}, session=session)
            session.commit_transaction()
            print("Transaction succeeded!")
    except DuplicateKeyError as e:
        print("Transaction failed and rolled back due to duplicate key:", e)

    finally:
        # Check if any document with order_id=1 exists
        count = collection.count_documents({"order_id": 1})
        print("Number of documents with order_id 1:", count)

