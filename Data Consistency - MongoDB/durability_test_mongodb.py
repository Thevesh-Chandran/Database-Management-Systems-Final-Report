from pymongo import MongoClient, WriteConcern

# Connect to MongoDB replica set
client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
db = client.get_database("mydb")

collection = db.get_collection("sales", write_concern=WriteConcern("majority"))

doc = {"order_id": 888888, "item_type": "DurabilityTest", "units_sold": 50}
result = collection.insert_one(doc)

print(f"Transaction committed. Document ID: {result.inserted_id}")
print("You can now restart the MongoDB node and check if it persists.")
