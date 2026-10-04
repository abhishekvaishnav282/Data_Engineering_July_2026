# Databricks notebook source
bronze_df = spark.read.format("delta").load("/Volumes/citibike_dev/citibike/citibike_bronze")
# bronze_df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import date_format,unix_timestamp

silver_df = bronze_df.select('ride_id', 'started_at', 'ended_at', 'start_station_name', 'end_station_name')
silver_df = silver_df.withColumn('trip_start_date', date_format("started_at", 'yyyy-MM-dd')) \
                    .withColumn("trip_duration_min", (unix_timestamp("ended_at") - unix_timestamp('started_at') )/60 )

# silver_df.select('trip_duration_min').show(10, False)

# COMMAND ----------

silver_df.write.format("delta").save('/Volumes/citibike_dev/citibike/citibike_silver')