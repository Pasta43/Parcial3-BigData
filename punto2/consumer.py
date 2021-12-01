from pyspark.sql import SparkSession
import pyspark.sql.functions as f
def entrega():
    print("¡Entrego!")
spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .getOrCreate()

lines = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers","localhost:9092") \
    .option("subscribe","quickstart-events") \
    .option("batchDuration","10")\
    .load()
df=lines.withColumn("Price", f.conv(f.col("value"), 16, 16).cast("bigint"))
#lines=KafkaUtils.createDirectStream(ssc,topics=['quickstart-events'],kafkaParams={'metadata.broker.list':'localhost:9092'})
#lines = ssc.socketTextStream("localhost", 9898)

df2 = df.select("Price")
dfPrice=df2.select(f.min("Price").alias("minPrice"),
                    f.max("Price").alias("maxPrice"),
                    f.avg("Price").alias("mean"),
                    #f.element_at('Price',-1).cast('bigint').alias("current"),
                    f.stddev("Price").alias('deviation'))#.withColumn("alert1",f.col("current")>2*f.col('deviation')+f.col('mean'))

query = dfPrice \
    .writeStream \
    .foreach(entrega)\
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()