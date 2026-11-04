import sys

from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

# --------------------------------------------------
# 1. INITIALIZE AWS GLUE AND SPARK
# --------------------------------------------------

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# --------------------------------------------------
# 2. DEFINE S3 PATHS
# --------------------------------------------------

RAW_PATH = "s3://etl-bucket-sample-2026/raw/"
OUTPUT_PATH = "s3://etl-bucket-sample-2026/processed/"

# --------------------------------------------------
# 3. EXTRACT: READ RAW CSV
# --------------------------------------------------

sales_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "false")
    .csv(RAW_PATH)
)

# --------------------------------------------------
# 4. TRANSFORM: APPLY DATA TYPES
# --------------------------------------------------

sales_df = (
    sales_df
    .withColumn("sale_date", F.to_date("sale_date", "yyyy-MM-dd"))
    .withColumn("quantity", F.col("quantity").cast("integer"))
    .withColumn("unit_price", F.col("unit_price").cast("decimal(12,2)"))
    .withColumn("sales_amount", F.col("sales_amount").cast("decimal(14,2)"))
    .cache()
)

# --------------------------------------------------
# 5. DATA QUALITY: FILTER INVALID SALES
# --------------------------------------------------

valid_sales = (
    sales_df
    .filter(
        (F.col("sales_amount") > 0) &
        (F.col("quantity") > 0) &
        F.col("sale_id").isNotNull() &
        F.col("product_id").isNotNull() &
        F.col("sale_date").isNotNull()
    )
    .cache()
)

source_count = sales_df.count()
valid_count = valid_sales.count()
rejected_count = source_count - valid_count

# --------------------------------------------------
# 6. CREATE PRODUCT DIMENSION TABLE
# --------------------------------------------------

dim_product = (
    valid_sales
    .groupBy("product_id")
    .agg(
        F.first("product_name", ignorenulls=True).alias("product_name"),
        F.first("category", ignorenulls=True).alias("category")
    )
    .withColumn("product_key", F.xxhash64("product_id"))
    .select(
        "product_key",
        "product_id",
        "product_name",
        "category"
    )
)

# --------------------------------------------------
# 7. CREATE SALES FACT TABLE
# --------------------------------------------------

fact_sales = (
    valid_sales
    .join(
        dim_product.select("product_id", "product_key"),
        on="product_id",
        how="inner"
    )
    .select(
        "sale_id",
        "product_key",
        "sale_date",
        "quantity",
        "unit_price",
        "sales_amount"
    )
)

# --------------------------------------------------
# 8. LOAD: WRITE PARQUET FILES TO S3
# --------------------------------------------------

dim_product.write \
    .mode("overwrite") \
    .parquet(OUTPUT_PATH + "dim_product/")

fact_sales.write \
    .mode("overwrite") \
    .parquet(OUTPUT_PATH + "fact_sales/")

# --------------------------------------------------
# 9. VALIDATE ETL RESULTS
# --------------------------------------------------

print("========== SALES ETL REPORT ==========")

print("Source records:", source_count)
print("Valid sales:", valid_count)
print("Rejected sales:", rejected_count)

print("Product dimension records:", dim_product.count())

fact_sales.agg(
    F.sum("quantity").alias("total_quantity"),
    F.sum("sales_amount").alias("total_revenue")
).show()

print("ETL PROCESS COMPLETED SUCCESSFULLY")

sales_df.unpersist()
valid_sales.unpersist()

job.commit()
