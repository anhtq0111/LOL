from pyspark.sql import SparkSession
from pyspark.sql.functions import *

mongodb_uri = "mongodb+srv://1:1@bigdata.drwtiay.mongodb.net/?retryWrites=true&w=majority"
Database = "Bigdata"

spark = SparkSession\
        .builder.master("spark://spark-master:7077")\
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.2.1") \
        .config("spark.mongodb.read.connection.uri", mongodb_uri) \
        .config("spark.mongodb.write.connection.uri", mongodb_uri) \
        .appName("test")\
        .getOrCreate()

def write_data(df, db, cl):
    df.write.format("com.mongodb.spark.sql.connector.MongoTableProvider")\
        .option("database", db)\
        .option("collection", cl)\
        .mode("append")\
        .save()

# Đọc dữ liệu từ HDFS
df = spark.read.json("hdfs://namenode:8020/data", recursiveFileLookup=True)
main_df = df.select('championName', 'teamPosition', 'visionScore', 'kills', 'deaths', 'assists', 'win')
main_df.createOrReplaceTempView("df_sql")

# Xử lý cái lỗi chả hiểu sao có 
query1 = """
SELECT *
FROM df_sql
WHERE championName is not NULL
"""
df_main = spark.sql(query1)
write_data(df_main, Database, "main")

# Tính tỉ lệ win của từng champion

query2 = """
SELECT
  championName,
  COUNT(*) AS total,
  COUNT(CASE WHEN win THEN 1 ELSE NULL END) AS wins
FROM df_sql
WHERE championName is not NULL
GROUP BY championName
ORDER BY total DESC
"""
df_winrate = spark.sql(query2)
df_winrate = df_winrate.withColumn("winrate", col("wins") / col("total") * 100)
# df_winrate.show(5)
write_data(df_winrate, Database, "winrate")


# Máy yếu quá nên thôi bỏ đi 

# # Extract dữ liệu theo lane 
# # Top
# top_df = main_df.filter(main_df["teamPosition"] == "TOP")
# write_data(top_df, Database, "top")

# # Rừng
# jg_df = main_df.filter(main_df["teamPosition"] == "JUNGLE")
# write_data(jg_df, Database, "jg")

# # Mid
# mid_df = main_df.filter(main_df["teamPosition"] == "MIDDLE")
# write_data(mid_df, Database, "mid")

# # Adc
# ad_df = main_df.filter(main_df["teamPosition"] == "BOTTOM")
# write_data(ad_df, Database, "ad")

# # Support
# sp_df = main_df.filter(main_df["teamPosition"] == "UTILITY")
# write_data(sp_df, Database, "sp")
