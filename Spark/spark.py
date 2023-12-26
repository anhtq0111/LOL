from pyspark.sql import SparkSession
from pyspark.sql.functions import *

mongodb_uri = "mongodb+srv://1:1@bigdata.drwtiay.mongodb.net/?retryWrites=true&w=majority"

spark = SparkSession\
        .builder.master("spark://spark-master:7077")\
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.2.1") \
        .config("spark.mongodb.read.connection.uri", mongodb_uri) \
        .config("spark.mongodb.write.connection.uri", mongodb_uri) \
        .appName("test")\
        .getOrCreate()

df = spark.read.json("hdfs://namenode:8020/data/Match11_player5.json")
newdf = df.select(df['championName'], df['teamPosition'], df['win'])

newdf.write.format("com.mongodb.spark.sql.connector.MongoTableProvider")\
        .option("database", "test")\
        .option("collection", "player")\
        .mode("append")\
        .save()
# newdf.show()