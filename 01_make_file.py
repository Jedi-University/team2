# python make_file.py bitcoin 365
import sys
import requests
import json
import os
import shutil

coin = "ethereum" if (len(sys.argv) <= 1) else sys.argv[1]
period = "365" if (len(sys.argv) <= 2) else sys.argv[2]

url = (
    "https://api.coingecko.com/api/v3/coins/"
    + coin
    + "/ohlc?vs_currency=usd&days="
    + period
)
response_API = requests.get(url)
dirname = "coin_folder"
filename = "ohlc.txt"
filepath = dirname + "/" + filename

try:
    os.remove(filepath)
except OSError:
    pass

try:
    shutil.rmtree(dirname)
except OSError:
    pass

os.mkdir(dirname)

to_file = response_API.text
with open(filepath, "w") as f:
    f.write(to_file)
