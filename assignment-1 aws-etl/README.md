# AWS Sales ETL Pipeline Using PySpark

![AWS](https://img.shields.io/badge/Cloud-AWS-orange)
![Python](https://img.shields.io/badge/Language-Python-blue)
![Apache Spark](https://img.shields.io/badge/Processing-PySpark-red)
![Athena](https://img.shields.io/badge/Analytics-Amazon%20Athena-purple)
![Storage](https://img.shields.io/badge/Storage-Amazon%20S3-green)

## 1. Project Overview

This project implements an end-to-end Sales Data ETL pipeline using Amazon Web Services (AWS).

The pipeline extracts raw sales transaction data from Amazon S3, processes and transforms it using AWS Glue with PySpark, and stores the transformed datasets in Parquet format. Amazon Athena is then used to query the processed data and generate analytical sales reports.

The main objective is to demonstrate practical knowledge of cloud-based data engineering, ETL processing, data warehousing, and SQL analytics.

## 2. Architecture

**Pipeline Flow:**

Amazon S3 → AWS Glue Crawler → AWS Glue Data Catalog → AWS Glue PySpark ETL → Amazon S3 (Parquet) → Amazon Athena

### AWS Services Used

| Service | Purpose |
|---|---|
| Amazon S3 | Stores raw CSV and processed Parquet datasets |
| AWS Glue Crawler | Automatically discovers the source CSV schema |
| AWS Glue Data Catalog | Stores database and table metadata |
| AWS Glue ETL | Executes the PySpark transformation job |
| PySpark | Performs data cleaning and transformation |
| Amazon Athena | Executes SQL queries on processed Parquet data |
| Amazon CloudWatch | Monitors Glue job execution and logs |

## 3. Dataset Description

The project uses a sample sales transaction dataset containing the following columns:

| Column | Description |
|---|---|
| sale_id | Unique sales transaction identifier |
| sale_date | Date of transaction |
| product_id | Product identifier |
| product_name | Product name |
| category | Product category |
| quantity | Number of units sold |
| unit_price | Price per unit |
| sales_amount | Total transaction amount |

The sample dataset contains 8 sales records, including one zero-dollar transaction.

## 4. ETL Process

### Step 1: Extract

- Uploaded the raw `sales.csv` dataset to Amazon S3.
- Configured an AWS Glue Crawler to discover the CSV schema.
- Registered the source table in the AWS Glue Data Catalog.

### Step 2: Transform

Implemented the transformation logic using PySpark in AWS Glue.

The transformations include:

- Reading CSV data from Amazon S3.
- Converting columns into appropriate data types.
- Filtering out zero-dollar sales.
- Removing records with invalid quantities or missing required fields.
- Creating a Product Dimension table.
- Creating a Sales Fact table.
- Generating a deterministic product key using `xxhash64()`.

### Step 3: Load

Stored the transformed datasets in Amazon S3 using Parquet format.

**Output structure:**

```text
processed/
├── dim_product/
│   └── Parquet files
└── fact_sales/
    └── Parquet files
```

## 5. Data Warehouse Design

The project uses a simple dimensional data model.

### Product Dimension – dim_product

| Column | Description |
|---|---|
| product_key | Generated product key |
| product_id | Original product identifier |
| product_name | Product name |
| category | Product category |

### Sales Fact – fact_sales

| Column | Description |
|---|---|
| sale_id | Transaction identifier |
| product_key | Reference to the product dimension |
| sale_date | Transaction date |
| quantity | Quantity sold |
| unit_price | Price per unit |
| sales_amount | Total sales amount |

## 6. Data Quality Rules

The following validation conditions were applied:

- Sales amount must be greater than zero.
- Quantity must be greater than zero.
- Sale ID must not be null.
- Product ID must not be null.
- Sale date must be valid.

Zero-dollar and invalid sales records were excluded from the final fact table.

## 7. Final Results

| Metric | Result |
|---|---:|
| Total source records | 8 |
| Valid sales records | 7 |
| Rejected records | 1 |
| Total quantity sold | 27 |
| Total revenue | 160,500 |

### Product-wise Sales Report

| Product | Category | Quantity | Revenue |
|---|---|---:|---:|
| Laptop | Electronics | 3 | 150,000 |
| Keyboard | Accessories | 5 | 5,000 |
| Mouse | Accessories | 9 | 4,500 |
| USB Cable | Accessories | 10 | 1,000 |
| **Total** | | **27** | **160,500** |

## 8. Repository Structure

```text
aws-sales-etl-pyspark/
│
├── README.md
│
├── data/
│   └── sales.csv
│
├── scripts/
│   └── sales_etl1.py
│
├── sql/
│   ├── create_tables.sql
│   └── sales_report.sql
│
└── screenshots/
    ├── glue_job_configuration.png
    ├── glue_job_success.png
    └── athena_sales_report.png
```

## 9. How to Reproduce the Project

1. Create an Amazon S3 bucket.
2. Upload the sample sales CSV file.
3. Create an AWS Glue Data Catalog database.
4. Configure and run an AWS Glue Crawler.
5. Create an AWS Glue PySpark ETL job.
6. Execute the ETL script to generate the fact and dimension datasets.
7. Store the processed Parquet files in Amazon S3.
8. Register the Parquet datasets as external tables in Amazon Athena.
9. Execute the SQL queries to generate sales reports.

The AWS Glue script and SQL files required for reproducing the pipeline are included in this repository.

## 10. Execution Evidence

The `screenshots/` directory contains genuine screenshots captured during the project execution:

- AWS Glue job configuration.
- Successful AWS Glue ETL execution.
- Final Amazon Athena sales aggregation report.

## 11. Cost Management

The project was implemented using AWS services with attention to resource usage.

- Glue jobs and crawlers were executed manually.
- No recurring schedules were configured.
- AWS resources were deleted after successful execution to avoid further resource-related charges.

Actual AWS charges depend on service usage, region, account allowances and promotional credits.

## 12. Key Learnings

Through this project, I gained practical experience in:

- Cloud-based ETL pipeline development.
- AWS S3 data storage.
- AWS Glue Crawlers and Data Catalog.
- PySpark transformations.
- Data quality validation.
- Fact and Dimension modelling.
- Parquet data storage.
- Amazon Athena SQL analytics.
- IAM permissions and AWS resource management.

## 13. Author

**Balaji Suriya V.**

Aspiring Cloud Data Engineer

**Technologies:** AWS | Python | PySpark | SQL | Apache Spark | Data Engineering