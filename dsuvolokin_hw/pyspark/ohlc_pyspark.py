import requests
import json
import sys
from os import path
from shutil import rmtree 
from pyspark import SparkContext
from pyspark.sql import SparkSession,Row
from pyspark.sql.window import *
from pyspark.sql.functions import row_number,col,expr,avg
from pyspark.sql.types import IntegerType

sc = SparkContext('local')
spark = SparkSession(sc)

filepath = 'coinfolder'

coin = "ethereum" if (len(sys.argv) <= 1) else sys.argv[1]
period = "365" if (len(sys.argv) <= 2) else sys.argv[2]

url = (
    "https://api.coingecko.com/api/v3/coins/"
    + coin
    + "/ohlc?vs_currency=usd&days="
    + period
)
response = requests.get(url)
l = json.loads(response.text)

rdd = sc.parallelize(l)
r=Row('time','open','high','low','close')
df = rdd.toDF(r)

grouped_df = (
    df
    .withColumn('rn',row_number().over(Window.orderBy('time')))
    # .withColumn('block_stamp',expr('cast((rn-1)/30 as int)'))
    # .withColumn('mean_over_block',avg('close').over(Window.partitionBy('block_stamp'))) # вычисление для блоков по 30 записей
    .withColumn('close_sma30', avg('close').over(Window().orderBy('rn').rangeBetween(-30,0))) # вычисление скользящей по 30 записей
    .withColumn('profit',expr('close-close_sma30'))
    .filter('close > close_sma30')
    .select('time','open','high','low','close','profit')
    )

if path.isdir(filepath):
    try:
      rmtree(f"{filepath}", ignore_errors=True)
    except Exception as e:
      print(e)

grouped_df.repartition(1).write.csv(filepath,header='true')
