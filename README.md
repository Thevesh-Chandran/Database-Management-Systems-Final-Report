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

### 2. Performance Testing
```bash
# CockroachDB
python "Performance - CockroachDB/performance.py"

# MongoDB
python "Performance - MongoDB/performance.py"
