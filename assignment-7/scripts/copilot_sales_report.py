
import sqlite3
from pathlib import Path

# Define the local database location
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "sales.db"


def create_database():

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Create product dimension table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_key INTEGER PRIMARY KEY,
            product_id TEXT,
            product_name TEXT,
            category TEXT
        )
    """)

    # Create sales fact table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_sales (
            sale_id INTEGER PRIMARY KEY,
            product_key INTEGER,
            quantity INTEGER,
            sales_amount REAL,
            FOREIGN KEY (product_key)
                REFERENCES dim_product(product_key)
        )
    """)

    # Insert sample product records
    cursor.execute("DELETE FROM fact_sales")
    cursor.execute("DELETE FROM dim_product")

    cursor.executemany("""
        INSERT INTO dim_product VALUES (?, ?, ?, ?)
    """, [
        (1, "P101", "Laptop", "Electronics"),
        (2, "P102", "Mouse", "Accessories"),
        (3, "P103", "Keyboard", "Accessories"),
        (4, "P104", "Monitor", "Electronics")
    ])

    # Insert sample sales transactions
    cursor.executemany("""
        INSERT INTO fact_sales VALUES (?, ?, ?, ?)
    """, [
        (1, 1, 2, 100000),
        (2, 2, 5, 2500),
        (3, 3, 3, 3000),
        (4, 1, 1, 50000),
        (5, 2, 4, 2000),
        (6, 4, 2, 30000)
    ])

    connection.commit()
    connection.close()

    print("Dummy sales database created successfully!")


if __name__ == "__main__":
    create_database()

# Generate a monthly sales report using the star schema.
# Join fact_sales with dim_product using product_key.
# Select product_name and category from dim_product.
# Calculate total_quantity using SUM of fact_sales.quantity.
# Calculate total_revenue using SUM of fact_sales.sales_amount.
# Group the results by product_name and category.
# Sort the results by total_revenue in descending order.