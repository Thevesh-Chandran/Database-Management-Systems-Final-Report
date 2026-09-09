# Experiment setup guide

Preserved coursework setup notes. Run each script from its corresponding experiment folder and adjust dataset paths and database settings for your machine. These experiments modify database records; use dedicated local test databases. The commands assume the required database binaries are installed.

## Steps to Run

### 1. Prepare Dataset
Place `sales_data.csv` in the root of the repository or adjust paths in the scripts.

# Performance Testing Steps

## CockroachDB
1. **Start the database:** Open PowerShell and start a single-node CockroachDB instance.  
   ```powershell
   cockroach start-single-node --insecure --listen-addr=localhost:26257 --http-addr=8081
   ```

2. **Connect to SQL shell:**
 ```powershell
cockroach sql --insecure --host=localhost:26257
   ```
3. **Create database and table: Run SQL commands to create nordstrom database and sales_data table**
 ```powershell
CREATE DATABASE nordstrom;
USE nordstrom;

CREATE TABLE sales_data (
    region STRING,
    country STRING,
    item_type STRING,
    sales_channel STRING,
    order_priority STRING,
    order_date DATE,
    order_id INT PRIMARY KEY,
    ship_date DATE,
    units_sold INT,
    unit_price DECIMAL,
    unit_cost DECIMAL,
    total_revenue DECIMAL,
    total_cost DECIMAL,
    total_profit DECIMAL
);

   ```

4. **Run performance script**
 ```powershell
python performance_test_cockroachdb.py
   ```
---

## MongoDB
1. **Install Python MongoDB driver**
 ```powershell
pip install pymongo
 ```
2. **Run performance script**
```powershell
python performance_test_mongodb.py
 ```
---

# Scalability Testing Steps

## CockroachDB
1. **Create directories for each node**
   ```powershell
   mkdir node1
   mkdir node2
   mkdir node3
    ```
   
2. **Start node 1**
 ```powershell
cockroach start --insecure --store=node1 --listen-addr=localhost:26257
   ```

3. **Start node 2 (Do this on a new terminal and do not close any other terminal)**
 ```powershell
cockroach start --insecure --store=node2 --listen-addr=localhost:26258 --http-addr=localhost:8082 --join=localhost:26257
   ```

4. **Start node 3 (Do this on a new terminal and do not close any other terminal)**
 ```powershell
cockroach start --insecure --store=node3 --listen-addr=localhost:26259 --http-addr=localhost:8083 --join=localhost:26257
   ```

5. **Initialize the cluster**
```powershell
cockroach init --insecure --host=localhost:26257
   ```

6. **Run scalability test script**
```powershell
python scalability_test_cockroachdb.py
   ```
---

## MongoDB (Sharded Cluster Setup)
1. **Connect to config server / mongos**
 ```powershell
& "C:\Program Files\MongoDB\Server\8.2\bin\mongosh.exe" --port 27020
 ```
2. **Connect to shard 1**
```powershell
& "C:\Program Files\MongoDB\Server\8.2\bin\mongosh.exe" --port 27021
 ```

3. **Connect to shard 2 (Do this on a new terminal and do not close any other terminal)**
 ```powershell
& "C:\Program Files\MongoDB\Server\8.2\bin\mongosh.exe" --port 27022
   ```

4. **Connect to shard 3 (Do this on a new terminal and do not close any other terminal)**
 ```powershell
& "C:\Program Files\MongoDB\Server\8.2\bin\mongosh.exe" --port 27023
   ```

5. **Run the following commands inside mongosh to configure sharding (Do this on a new terminal and do not close any other terminal)**
```powershell
sh.addShard("shard1/localhost:27021")
sh.addShard("shard2/localhost:27022")
sh.addShard("shard3/localhost:27023")
   ```

6. **Run scalability test script**
```powershell
python scalability_test_mongodb.py
   ```
---

# Data Consistency Testing (ACID)
## CockroachDB
## Atomicity Test – CockroachDB

1. **start the single-node CockroachDB instance**
```powershell
cockroach start-single-node --insecure --listen-addr=localhost:26257 --http-addr=8081
```
2. **Create and connect to the database and table**
```powershell
CREATE DATABASE IF NOT EXISTS nordstrom;
\c nordstrom;

CREATE TABLE IF NOT EXISTS sales_data (
    order_id INT PRIMARY KEY,
    item_type STRING,
    units_sold INT
);
```
3. **Run atomicity test script**
```powershell
python atomicity_test.py
```

4. **Verify rollback (record should NOT exist)**
```powershell
SELECT * FROM sales_data WHERE order_id = 999999;
```
---

## Consistency Test – CockroachDB


1. **start the single-node CockroachDB instance**
```powershell
cockroach start-single-node --insecure --listen-addr=localhost:26257 --http-addr=8081
```
2. **Run consistency test script**
```powershell
python consistency_test.py
```
### Note:
### The test triggers a duplicate key constraint violation
### because order_id = 1 already exists and violates the primary key rule.

---

## Isolation Test – CockroachDB

1. **start the single-node CockroachDB instance**
```powershell
cockroach start-single-node --insecure --listen-addr=localhost:26257 --http-addr=8081
```
2. **Run isolation test script**
```powershell
python isolation_test.py
```

4. **When prompted, press ENTER to resume Transaction 1**
### (Transaction 1 is intentionally paused to test isolation)

5. ** Verify final value**
```powershell
SELECT * FROM sales_data WHERE order_id = 1;
```
### units_sold should be 15

---

## Durability Test – CockroachDB

1. **start the single-node CockroachDB instance**
```powershell
cockroach start-single-node --insecure --listen-addr=localhost:26257 --http-addr=8081
```
2. **Run durability test script**
```powershell
python durability_test.py
```

3. **Restart the node**
### Close the terminal, then start the single-node CockroachDB instance again (repeat step 1)

4. **Verify the record persists**
```powershell
SELECT * FROM sales_data WHERE order_id = 888888;
```
### units_sold should be 50

---

## MongoDB
## Atomicity Test – MongoDB

1. **Step 1: Start MongoDB as a replica set (required for transactions)**
```powershell
mongod --dbpath C:\data\mongodb --replSet rs0 --port 27017
```
2. **Open a NEW terminal and connect to MongoDB shell**
```powershell
mongosh --port 27017
```

3. **Initialize the replica set (run inside mongosh)**
```powershell
rs.initiate()
```
4. **Run atomicity test script**
```powershell
python atomicity_test_mongodb.py
```
### The script will automatically state the number of documents with order_id 999999, which should be 0 ( not exists)

## Consistency Test – MongoDB

1. **Step 1: Start MongoDB as a replica set (required for transactions)**
```powershell
mongod --dbpath C:\data\mongodb --replSet rs0 --port 27017
```
2. **Open a NEW terminal and connect to MongoDB shell**
```powershell
mongosh --port 27017
```

3. **Initialize the replica set (run inside mongosh)**
```powershell
rs.initiate()
```
4. **Run consistency test script**
```powershell
python consistency_test_mongodb.py
```
### Note: The script will automatically give an duplicate key constraint violation error and state the no of doucments with order id of 1 , which should be 0

---

## Isolation Test – MongoDB

1. **Step 1: Start MongoDB as a replica set (required for transactions)**
```powershell
mongod --dbpath C:\data\mongodb --replSet rs0 --port 27017
```
2. **Open a NEW terminal and connect to MongoDB shell**
```powershell
mongosh --port 27017
```

3. **Initialize the replica set (run inside mongosh)**
```powershell
rs.initiate()
```
4. **Run isolation test script**
```powershell
python isolation_test_mongodb.py
```

5. **When prompted, press ENTER to resume Transaction 1**
### (Transaction 1 is intentionally paused to test isolation)

### Note: The script will automatically state the units_sold for order id of 1, which should be 15

---

## Durability Test – MongoDB

1. **Step 1: Start MongoDB as a replica set (required for transactions)**
```powershell
mongod --dbpath C:\data\mongodb --replSet rs0 --port 27017
```
2. **Open a NEW terminal and connect to MongoDB shell**
```powershell
mongosh --port 27017
```

3. **Initialize the replica set (run inside mongosh)**
```powershell
rs.initiate()
```
4. **Run durability test script**
```powershell
python durability_test_mongodb.py
```

5. **Restart the node**
### Close the terminal, then start the single-node CockroachDB instance again (repeat step 1)

6. **Verify the record persists**
```powershell
use mydb
db.sales.find({ order_id: 888888 }).pretty()
```
### units_sold should be 50

---
