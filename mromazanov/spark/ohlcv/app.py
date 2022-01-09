from pyspark.sql.functions import avg, row_number,lit, udf

from pyspark.sql.window import Window
import requests
from pyspark.sql import SparkSession
from pyspark import SparkContext

@udf
def func(value, num):
    return value // num


if __name__ == "__main__":
    coin = "ethereum"
    days = 365
    schema = ["time", "open", "high", "low", "close"]

    ss = SparkSession.builder\
            .master("local[*]")\
            .appName('ohlcv')\
            .getOrCreate()

    sc = ss.sparkContext

    data = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency=usd&days={days}").json()
    rdd = sc.parallelize(data)
    df = ss.createDataFrame(rdd, schema=schema)

    order = Window.orderBy("time")
    partition = Window.partitionBy("group")

    df = df.withColumn("row", row_number().over(order))
    df = df.withColumn("group", func(df.row, lit(30)))
    df = df.withColumn("sma", avg("close").over(partition))

    df = df.filter(df["close"]>df["sma"])
    df.drop("row","group","sma")

    print(df.show(100))
    df.write.csv(path='./csv', header=True, sep=',')
