
-- ============================================
-- AWS SALES ETL PROJECT
-- SALES ANALYTICS REPORT
-- ============================================

USE `suriya-etl-2026-sample`;

-- ============================================
-- QUERY 1: PRODUCT-WISE SALES REPORT
-- ============================================

SELECT
    p.product_name,
    p.category,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales_amount) AS total_revenue
FROM fact_sales f
INNER JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.product_name,
    p.category
ORDER BY
    total_revenue DESC;


-- ============================================
-- QUERY 2: OVERALL SALES SUMMARY
-- ============================================

SELECT
    COUNT(*) AS valid_sales,
    SUM(quantity) AS total_quantity,
    SUM(sales_amount) AS total_revenue
FROM fact_sales;


-- ============================================
-- QUERY 3: CATEGORY-WISE REVENUE
-- ============================================

SELECT
    p.category,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales_amount) AS total_revenue
FROM fact_sales f
INNER JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.category
ORDER BY
    total_revenue DESC;


-- ============================================
-- QUERY 4: HIGHEST REVENUE PRODUCT
-- ============================================

SELECT
    p.product_name,
    SUM(f.sales_amount) AS total_revenue
FROM fact_sales f
INNER JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.product_name
ORDER BY
    total_revenue DESC
LIMIT 1;


-- ============================================
-- QUERY 5: SALES TRANSACTION DETAILS
-- ============================================

SELECT
    sale_id,
    sale_date,
    product_key,
    quantity,
    unit_price,
    sales_amount
FROM fact_sales
ORDER BY sale_date;
