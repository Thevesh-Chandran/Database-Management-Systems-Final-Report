# A Comparative Study of NoSQL and NewSQL Databases: Scalability, Consistency, and Performance Analysis

> MAKE SURE TO READ THE ENTIRE REPOSITORY. THE STEPS GUIDE IS AT THE BOTTOM.

This repository contains all code, scripts, and instructions for reproducing the experiments conducted in the research on evaluating **NewSQL (CockroachDB)** and **NoSQL (MongoDB)** databases. The experiments focus on **performance, scalability, and data consistency (ACID properties)** using a controlled dataset of 100,000 sales records.

---

## Repository Structure

- **Dataset:** `sales_data.csv`  
- **Folders:**
  1. **Performance - CockroachDB**: Python scripts for performance testing on CockroachDB  
  2. **Performance - MongoDB**: Python scripts for performance testing on MongoDB  
  3. **Scalability - CockroachDB**: Python scripts for scalability testing on CockroachDB  
  4. **Scalability - MongoDB**: Python scripts for scalability testing on MongoDB  
  5. **Data Consistency - CockroachDB**: Python scripts for atomicity, durability, isolation, and consistency testing on CockroachDB  
  6. **Data Consistency - MongoDB**: Python scripts for atomicity, durability, isolation, and consistency testing on MongoDB  

---

## Methodology Overview

### Research Design
- **Type:** Quantitative experimental comparative study  
- **Objective:** Evaluate and compare **performance, scalability, and consistency** of CockroachDB (NewSQL) and MongoDB (NoSQL)  
- **Metrics:**  
  - **Performance:** Latency, write/read throughput, aggregation latency  
  - **Scalability:** Throughput with 1-node, 2-node, 3-node clusters/shards  
  - **Consistency:** ACID properties (Atomicity, Consistency, Isolation, Durability)  

### Data Collection
- Dataset: 100,000-row structured sales data CSV from Kaggle  
- Inserted in **batches of 5,000 rows**  
- Python scripts automate insertion, read, and aggregation operations  

### Experimental Setup
- **Hardware:** ASUS Vivobook 15X OLED, AMD Ryzen 7-7730U, 16GB RAM, 512GB SSD  
- **Software:** Windows 11, Python, CockroachDB, MongoDB, Microsoft Office  
- **Environment:** Single-node and multi-node CockroachDB clusters, sharded MongoDB clusters  

---

## Implementation Details

### 1. Performance Testing
- **CockroachDB:** Single-node batch insertions using Python `execute_values`  
- **MongoDB:** Batch inserts as documents using Python PyMongo  
- Metrics: write latency, write throughput, read latency, read throughput, aggregation latency  

### 2. Scalability Testing
- **CockroachDB:** Tested with 1, 2, and 3-node clusters  
- **MongoDB:** Tested with 1, 2, and 3-shard clusters  
- Metrics: write/read throughput, scaling factors  

### 3. Data Consistency Testing
- **Atomicity:** Transaction rollback on primary key violation  
- **Consistency:** Database constraints enforced during insertions  
- **Isolation:** Two concurrent transactions on the same record  
- **Durability:** Record survives node restart  

---

## Tools and Technologies
- **Python**: Automation, performance measurement, and ACID testing  
- **CockroachDB**: NewSQL database  
- **MongoDB**: NoSQL database  
- **PowerShell**: CockroachDB node startup and MongoDB shard configuration  
- **Kaggle CSV Dataset**: Sales data for experiments  

---

## Steps to Run

### 1. Prepare Dataset
Place `sales_data.csv` in the root of the repository or adjust paths in the scripts.

## Performance Testing Steps

### CockroachDB
1. **Start the database:** Open PowerShell and start a single-node CockroachDB instance.  
   ```powershell
   cockroach start-single-node --insecure --listen-addr=localhost:26257 --http-addr=8081
   
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
### MongoDB
1. **Install Python MongoDB driver**
 ```powershell
pip install pymongo
 ```
2. **Run performance script**
```powershell
python performance_test_mongodb.py
 ```

## Scalability Testing Steps

### CockroachDB
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

### MongoDB (Sharded Cluster Setup)
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

## Data Consistency Testing (ACID)
### Atomicity Test – CockroachDB

1. **Create and connect to the database and table**
```powershell
CREATE DATABASE IF NOT EXISTS nordstrom;
\c nordstrom;

CREATE TABLE IF NOT EXISTS sales_data (
    order_id INT PRIMARY KEY,
    item_type STRING,
    units_sold INT
);
```
2. **Run atomicity test script**
```powershell
python atomicity_cockroachdb.py
```

3. **Verify rollback (record should NOT exist)**
```powershell
SELECT * FROM sales_data WHERE order_id = 999999;
```

## Consistency Test – CockroachDB

1. **Run consistency test script**
```powershell
python consistency_cockroachdb.py
```
##Note:
##The test triggers a duplicate key constraint violation
##because order_id = 1 already exists and violates the primary key rule.


python isolation_cockroachdb.py
python durability_cockroachdb.py

# MongoDB ACID tests
python atomicity_mongodb.py
python consistency_mongodb.py
python isolation_mongodb.py
python durability_mongodb.py
