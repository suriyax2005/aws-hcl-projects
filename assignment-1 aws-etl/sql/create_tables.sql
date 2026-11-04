
-- ============================================
-- AWS SALES ETL PROJECT
-- CREATE ATHENA EXTERNAL TABLES
-- Database: suriya-etl-2026-sample
-- ============================================

-- Select the Glue Data Catalog database
USE `suriya-etl-2026-sample`;

-- ============================================
-- 1. PRODUCT DIMENSION TABLE
-- ============================================

CREATE EXTERNAL TABLE IF NOT EXISTS dim_product (
    product_key BIGINT,
    product_id STRING,
    product_name STRING,
    category STRING
)
STORED AS PARQUET
LOCATION
's3://etl-bucket-sample-2026/processed/dim_product/';

-- ============================================
-- 2. SALES FACT TABLE
-- ============================================

CREATE EXTERNAL TABLE IF NOT EXISTS fact_sales (
    sale_id STRING,
    product_key BIGINT,
    sale_date DATE,
    quantity INT,
    unit_price DECIMAL(12,2),
    sales_amount DECIMAL(14,2)
)
STORED AS PARQUET
LOCATION
's3://etl-bucket-sample-2026/processed/fact_sales/';

-- ============================================
-- VERIFY TABLES
-- ============================================

SHOW TABLES;
