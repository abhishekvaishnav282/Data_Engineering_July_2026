# Databricks notebook source
from pyspark.sql.types import StructType, StructField, DecimalType, StringType, TimestampType

citibike_schema = StructType([
    StructField('ride_id', StringType(), True),
    StructField('rideable_type', StringType(), True),
    StructField('started_at', TimestampType(), True),
    StructField('ended_at', TimestampType(), True),
    StructField('start_station_name', StringType(), True),
    StructField('start_station_id', StringType(), True),
    StructField('end_station_name', StringType(), True),
    StructField('end_station_id', StringType(), True),
    StructField('start_lat', DecimalType(10, 10), True),
    StructField('start_lng', DecimalType(10, 10), True),
    StructField('end_lat', DecimalType(10, 10), True),
    StructField('end_lng', DecimalType(10, 10), True),
    StructField('member_casual', StringType(), True)
])
citibike_df = spark.read.schema(citibike_schema).csv("/Volumes/citibike_dev/citibike/landing", header = True)

# COMMAND ----------

citibike_df.write.mode('overwrite').save("/Volumes/citibike_dev/citibike/citibike_bronze")