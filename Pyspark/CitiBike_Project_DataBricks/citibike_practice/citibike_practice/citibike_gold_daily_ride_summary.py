# Databricks notebook source
silver_df = spark.read.format('delta').load('/Volumes/citibike_dev/citibike/citibike_silver')

# COMMAND ----------

from pyspark.sql.functions import min, max, avg, count

gold_df = silver_df.groupBy("trip_start_date").agg(max("trip_duration_min").alias("max_trip_duration_mins"),
                                                   min("trip_duration_min").alias("min_trip_duration_mins"),
                                                   avg("trip_duration_min").alias("avg_trip_duration_mins"),
                                                   count("trip_duration_min").alias("total_trips"),)

# COMMAND ----------

gold_df.write.format("delta").save('/Volumes/citibike_dev/citibike/citibike_gold/daily_ride_summary')