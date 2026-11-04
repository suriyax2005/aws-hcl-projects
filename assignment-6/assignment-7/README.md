# Assignment 07 – AI-Assisted SQL Query Generation Using GitHub Copilot

## 1. Project Overview

This project demonstrates the use of GitHub Copilot to generate SQL queries for a sales reporting system based on a dimensional data model (Star Schema).

The objective is to use descriptive comments and database schema information to guide GitHub Copilot in generating SQL SELECT, JOIN, and GROUP BY statements.

The generated SQL query is reviewed and verified before execution to ensure that the joins, aggregations, and grouping logic are correct.

## 2. Business Scenario

An e-commerce company wants to generate a sales report to understand product performance and revenue.

The report should display:

- Product names.
- Product categories.
- Total quantity sold.
- Total revenue generated.

A dummy SQLite database is created to simulate the company's sales data.

## 3. Database Design

The project uses two tables based on a simple Star Schema.

### 3.1 Fact Table – fact_sales

Stores transactional sales information.

| Column | Data Type | Description |
|---|---|---|
| sale_id | INTEGER | Unique sales transaction ID |
| product_key | INTEGER | Foreign key referencing dim_product |
| quantity | INTEGER | Number of products sold |
| sales_amount | REAL | Total revenue from the transaction |

### 3.2 Dimension Table – dim_product

Stores descriptive product information.

| Column | Data Type | Description |
|---|---|---|
| product_key | INTEGER | Primary key |
| product_id | TEXT | Original product identifier |
| product_name | TEXT | Product name |
| category | TEXT | Product category |

### Relationship

The two tables are connected through:

`fact_sales.product_key = dim_product.product_key`

## 4. Role of GitHub Copilot

GitHub Copilot Chat is used as an AI coding assistant to generate SQL queries from descriptive programming comments and the database schema.

The comments describe the required analytical operations:

1. Join `fact_sales` with `dim_product` using `product_key`.
2. Retrieve product names and categories.
3. Calculate total quantity using `SUM(quantity)`.
4. Calculate total revenue using `SUM(sales_amount)`.
5. Group results by product name and category.
6. Sort results by total revenue in descending order.

GitHub Copilot generates a SQL query based on these requirements.

## 5. Generated SQL Query

The generated query is reviewed against the database schema before execution.

```sql
SELECT
    p.product_name,
    p.category,
    SUM(f.quantity) AS total_quantity,
    SUM(f.sales_amount) AS total_revenue
FROM fact_sales AS f
INNER JOIN dim_product AS p
    ON f.product_key = p.product_key
GROUP BY
    p.product_name,
    p.category
ORDER BY total_revenue DESC;
```

### SQL Logic Verification

| Operation | Verification |
|---|---|
| SELECT | Retrieves product name and category |
| JOIN | Uses the correct product_key relationship |
| SUM(quantity) | Calculates total units sold |
| SUM(sales_amount) | Calculates total sales revenue |
| GROUP BY | Groups results by product and category |
| ORDER BY | Sorts revenue from highest to lowest |

The generated SQL is checked for correct table names, column names, join conditions, and aggregation logic before execution.

## 6. Expected Query Results

Based on the sample database records:

| Product | Category | Total Quantity | Total Revenue |
|---|---|---:|---:|
| Laptop | Electronics | 3 | 150000 |
| Monitor | Electronics | 2 | 30000 |
| Mouse | Accessories | 9 | 4500 |
| Keyboard | Accessories | 3 | 3000 |

These results demonstrate product-level sales aggregation.

## 7. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| SQLite | Dummy relational database |
| SQLite3 | Python database connectivity |
| GitHub Copilot Chat | AI-assisted SQL generation |
| VS Code | Development environment |
| GitHub | Source code management and submission |

## 8. Project Structure

```text
Assignment-07/
│
├── README.md
│
├── scripts/
│   └── copilot_sales_report.py
│
├── database/
│   └── sales.db
│
└── screenshots/
    ├── copilot_suggestions.png
    └── sales_query_result.png
```

## 9. Execution Instructions

### Step 1 – Run the Python script

```bash
python scripts/copilot_sales_report.py
```

### Step 2 – Generate the SQL query

Use GitHub Copilot Chat with descriptive comments and the database schema to generate the required SQL query.

### Step 3 – Verify the generated query

Check the SELECT columns, JOIN condition, aggregate functions, GROUP BY columns, and sorting logic.

### Step 4 – Execute the query

Execute the verified SQL query against the SQLite database using Python's SQLite connectivity.

### Step 5 – Verify the results

Check that the product-level quantity and revenue totals match the expected results.

## 10. Execution Evidence

### GitHub Copilot SQL Generation

![Copilot SQL suggestions](screenshots/copilot_suggestions.png)

### Sales Query Execution Result

![Sales query result](screenshots/sales_query_result.png)

## 11. Key Learnings

Through this assignment, I learned:

- How to design a simple Star Schema using fact and dimension tables.
- How to use GitHub Copilot to generate SQL from descriptive comments.
- How SQL JOIN operations combine transactional and descriptive data.
- How aggregate functions calculate sales quantities and revenue.
- Why GROUP BY is required for analytical reporting.
- Why AI-generated SQL must be reviewed and validated before execution.
- How Python connects to and executes queries against a SQLite database.

---

**Assignment:** 07 – AI-Assisted SQL Query Generation  
**Domain:** Data Engineering and AI-Assisted Development  
**Author:** Balaji Suriya V.