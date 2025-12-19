# Performance, Scalability, and Consistency Evaluation of CockroachDB and MongoDB

This repository contains all code, scripts, and instructions for reproducing the experiments conducted in the research on evaluating **NewSQL (CockroachDB)** and **NoSQL (MongoDB)** databases. The experiments focus on **performance, scalability, and data consistency (ACID properties)** using a controlled dataset of 100,000 sales records.

---

## Repository Structure

/CockroachDB-MongoDB-Evaluation
│
├── /dataset
│ └── sales_data.csv # CSV dataset of 100,000 sales records from Kaggle
│
├── /scripts
│ ├── /cockroachdb
│ │ ├── performance.py # Batch insert, read, and aggregation performance scripts
│ │ ├── scalability.py # Multi-node cluster scalability scripts
│ │ └── consistency.py # ACID property testing (atomicity, consistency, isolation, durability)
│ │
│ ├── /mongodb
│ │ ├── performance.py # Batch insert, read, and aggregation performance scripts
│ │ ├── scalability.py # Sharded cluster scalability scripts
│ │ └── consistency.py # ACID property testing
│
├── /cockroachdb_setup
│ ├── node_startup.ps1 # PowerShell scripts to start single-node and multi-node clusters
│ └── db_setup.sql # SQL scripts to create database and sales_data table
│
├── /mongodb_setup
│ ├── mongod_shard_startup.ps1 # Commands to start MongoDB shards
│ ├── mongos_config.ps1 # Commands to configure sharded cluster
│ └── collection_setup.py # Python script to create collection and indexes
│
└── README.md # This file


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

## How to Run the Scripts

1. **Setup Databases**  
```powershell
# CockroachDB
./cockroachdb_setup/node_startup.ps1
# Then create database and table
./cockroachdb_setup/db_setup.sql
