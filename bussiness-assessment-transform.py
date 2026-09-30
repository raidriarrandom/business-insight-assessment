import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

order_items_df = spark.read.csv("s3://business-insight-assessment-499502048569/raw/dbo/order_items/", header=False, inferSchema=True).toDF("APP_NAME", "RESTAURANT_ID", "CREATION_TIME_UTC", "ORDER_ID", "USER_ID", "PRINTED_CARD_NUMBER", "IS_LOYALTY", "CURRENCY", "LINEITEM_ID", "ITEM_CATEGORY", "ITEM_NAME", "ITEM_PRICE", "ITEM_QUANTITY")

order_item_options_df = spark.read.csv("s3://business-insight-assessment-499502048569/raw/dbo/order_item_options/", header=False, inferSchema=True).toDF("ORDER_ID", "LINEITEM_ID", "OPTION_GROUP_NAME", "OPTION_NAME", "OPTION_PRICE", "OPTION_QUANTITY")

date_dim_df = spark.read.csv("s3://business-insight-assessment-499502048569/raw/dbo/date_dim/", header=False, inferSchema=True).toDF("date_key", "year", "month", "week", "day_of_week", "is_weekend", "is_holiday", "holiday_name")

order_items_df.printSchema()
order_items_df.show(5)

order_item_options_clean = order_item_options_df.join(
    order_items_df.select("ORDER_ID", "LINEITEM_ID"),
    on=["ORDER_ID", "LINEITEM_ID"],
    how="inner"
)

order_item_totals = order_item_options_clean.groupBy("ORDER_ID", "LINEITEM_ID").agg(
    F.sum(F.col("OPTION_PRICE") * F.col("OPTION_QUANTITY")).alias("OPTION_TOTAL")
)

order_items_with_options = order_items_df.join(
    order_item_totals, on=["ORDER_ID", "LINEITEM_ID"], how="left"
).fillna(0, subset=["OPTION_TOTAL"])

order_items_priced = order_items_with_options.withColumn(
    "LINE_TOTAL",
    (F.col("ITEM_PRICE") * F.col("ITEM_QUANTITY")) + F.col("OPTION_TOTAL")
)

order_items_valid_user = order_items_priced.filter(
    (F.col("USER_ID").isNotNull()) & (F.col("ITEM_PRICE") <= 100)
)

clv_df = order_items_valid_user.groupBy("USER_ID").agg(
    F.sum("LINE_TOTAL").alias("CUSTOMER_LIFETIME_VALUE"),
    F.count("ORDER_ID").alias("TOTAL_LINE_ITEMS"),
    F.min("CREATION_TIME_UTC").alias("FIRST_ORDER_DATE"),
    F.max("CREATION_TIME_UTC").alias("LAST_ORDER_DATE")
)

clv_df.printSchema()
clv_df.show(10)

clv_df.write.mode("overwrite").parquet("s3://business-insight-assessment-499502048569/curated/customer_lifetime_value/")

order_items_priced.write.mode("overwrite").parquet("s3://business-insight-assessment-499502048569/curated/order_items_enriched/")

order_frequency_df = order_items_valid_user.groupBy("USER_ID").agg(
    F.countDistinct("ORDER_ID").alias("ORDER_FREQUENCY")
)

sales_by_category_df = order_items_valid_user.groupBy("ITEM_CATEGORY").agg(
    F.sum("LINE_TOTAL").alias("TOTAL_SALES")
)

sales_by_loyalty_df = order_items_valid_user.groupBy("IS_LOYALTY").agg(
    F.sum("LINE_TOTAL").alias("TOTAL_SALES")
)

order_items_with_date = order_items_valid_user.join(
    date_dim_df,
    F.to_date(order_items_valid_user["CREATION_TIME_UTC"]) == date_dim_df["date_key"],
    how="inner"
)

sales_by_holiday_df = order_items_with_date.groupBy("is_holiday").agg(
    F.sum("LINE_TOTAL").alias("TOTAL_SALES")
)

order_frequency_df.write.mode("overwrite").parquet("s3://business-insight-assessment-499502048569/curated/order_frequency/")

sales_by_category_df.write.mode("overwrite").parquet("s3://business-insight-assessment-499502048569/curated/sales_by_category/")

sales_by_loyalty_df.write.mode("overwrite").parquet("s3://business-insight-assessment-499502048569/curated/sales_by_loyalty/")

sales_by_holiday_df.write.mode("overwrite").parquet("s3://business-insight-assessment-499502048569/curated/sales_by_holiday/")

job.commit()
