# Assignment 06 – Three-Layer Data Pipeline Using Pandas and SQLAlchemy

## 1. Project Overview

This project demonstrates the implementation of a simple automated data pipeline using Python, Pandas, SQLAlchemy, and SQLite.

The objective is to retrieve raw CSV data from a public URL, clean and transform the data, and store the processed records in a local SQLite database.

The pipeline follows three architectural layers:

1. Ingestion
2. Integration
3. Presentation

## 2. Dataset Information

**Dataset:** Apple Historical Stock Data

**Source:** [Public CSV Dataset](https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv)

The dataset contains historical stock market information, including:

- Date
- Opening price
- Highest price
- Lowest price
- Closing price
- Trading volume
- Moving averages and other financial indicators

## 3. Architecture and Implementation

### Layer 1 – Ingestion

**Library: Pandas**

The ingestion layer retrieves the raw CSV dataset directly from a public URL and loads it into a Pandas DataFrame.

**Function used:**

```python
pd.read_csv(DATA_URL)
```

Responsibilities:

- Read CSV data from the public URL.
- Load the data into a DataFrame.
- Inspect the dataset columns and initial records.

### Layer 2 – Integration

**Library: Pandas**

The integration layer cleans and transforms the raw dataset before storing it in the database.

**Functions used:**

```python
pd.to_datetime()
df.dropna()
df.fillna()
df.select_dtypes()
```

Data cleaning operations:

- Standardize the Date column using Pandas datetime conversion.
- Identify and remove records containing invalid dates.
- Fill missing numeric values using the respective column median.
- Fill missing text values with the value "Unknown".
- Verify that no missing values remain after cleaning.

### Layer 3 – Presentation

**Libraries: SQLAlchemy and SQLite**

The presentation layer stores the cleaned DataFrame in a local SQLite database.

**Functions used:**

```python
create_engine()
df.to_sql()
```

Implementation:

- Create a local SQLite database named `cleaned_data.db`.
- Establish a database connection using SQLAlchemy.
- Create a table named `stock_data`.
- Insert the cleaned records into the SQLite table.
- Verify the inserted records using DB Browser for SQLite.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | CSV ingestion and data transformation |
| SQLAlchemy | Database connectivity |
| SQLite | Local database storage |
| DB Browser for SQLite | Database verification |
| VS Code | Development environment |
| GitHub | Project version control and submission |

## 5. Project Execution

### Step 1 – Install Dependencies

```bash
python -m pip install pandas sqlalchemy
```

### Step 2 – Execute the Pipeline

```bash
python scripts/data_pipeline.py
```

### Step 3 – Verify the Database

Open `database/cleaned_data.db` using DB Browser for SQLite.

Select the `stock_data` table under Browse Data to verify the inserted records.

## 6. Project Structure

```text
Assignment-06/
│
├── README.md
│
├── scripts/
│   └── data_pipeline.py
│
├── database/
│   └── cleaned_data.db
│
└── screenshots/
    ├── terminal_success.png
    └── sqlite_final_data.png
```

## 7. Execution Evidence

### Successful Pipeline Execution

![Successful terminal execution](screenshots/terminal_success.png)

### Final SQLite Database Records

![SQLite database records](screenshots/sqlite_final_data.png)

## 8. Expected Outcome

The completed pipeline successfully demonstrates the movement of data through three architectural layers.

- Raw CSV data is ingested using Pandas.
- Data is cleaned and transformed using Pandas.
- Processed data is stored in SQLite through SQLAlchemy.

The final result is a local SQLite database containing the cleaned `stock_data` table.

## 9. Key Learnings

Through this assignment, I learned:

- How to read external CSV datasets directly into Pandas.
- How to standardize date columns and handle missing values.
- How to use Pandas for data cleaning and transformation.
- How SQLAlchemy connects Python applications with databases.
- How to store processed DataFrames in SQLite.
- How to implement a simple end-to-end data pipeline using a three-layer architecture.

---

**Assignment:** 06 – Three-Layer Data Pipeline  
**Domain:** Data Engineering  
**Author:** Balaji Suriya V.