
import pandas as pd

from sqlalchemy import create_engine
from pathlib import Path

# Public CSV dataset URL
DATA_URL = (
    "https://raw.githubusercontent.com/plotly/datasets/"
    "master/finance-charts-apple.csv"
)


def ingest_data():
    """
    Read raw CSV data from a public URL
    into a Pandas DataFrame.
    """

    print("INGESTION: Reading raw CSV data...")

    df = pd.read_csv(DATA_URL)

    print("Data successfully ingested!")
    print("Total records:", len(df))

    print("\nDataset columns:")
    print(df.columns.tolist())

    print("\nFirst five raw records:")
    print(df.head())

    return df


def transform_data(df):
    """
    Clean and transform the raw DataFrame.
    """

    print("\nINTEGRATION: Cleaning data...")

    # 1. Standardize the Date column
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # 2. Remove records with invalid dates
    df = df.dropna(subset=["Date"]).copy()

    # 3. Fill missing numeric values with column median
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:
        median_value = df[column].median()
        df[column] = df[column].fillna(median_value)

    # 4. Fill missing text values with Unknown
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        df[column] = df[column].fillna("Unknown")

    print("Data cleaning completed!")

    print("\nMissing values after cleaning:")
    print(df.isnull().sum())

    print("\nFirst five cleaned records:")
    print(df.head())

    return df


def load_data(df):
    """
    Load cleaned DataFrame into a local SQLite database.
    """

    print("\nPRESENTATION: Loading data into SQLite...")

    # Create database folder
    database_folder = (
        Path(__file__).resolve().parent.parent / "database"
    )

    database_folder.mkdir(parents=True, exist_ok=True)

    # Create SQLite database connection
    database_path = database_folder / "cleaned_data.db"

    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}"
    )

    # Load DataFrame into SQLite table
    df.to_sql(
        "stock_data",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Data successfully loaded into SQLite!")
    print("Database:", database_path)
    print("Table: stock_data")
    print("Total records inserted:", len(df))

    engine.dispose()


def main():

    print("========== THREE-LAYER DATA PIPELINE ==========")

    # INGESTION
    raw_df = ingest_data()

    # INTEGRATION
    cleaned_df = transform_data(raw_df)

    # PRESENTATION
    load_data(cleaned_df)

    print("\n========== PIPELINE COMPLETED SUCCESSFULLY ==========")


if __name__ == "__main__":
    main()
