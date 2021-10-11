import os
import json


def my_mean(data):  # incoming_array
    acc = 0
    for i in data:
        acc += i[4]
    return acc / len(data)


def my_filter(data):
    acc = []
    for i in data:
        acc.append(i) if i[4] > my_mean(data) else None
    return acc


dir_str = "coin_folder"
directory = os.fsencode(dir_str)
new_file = "advanced_ohlc.txt"
new_file_path = dir_str + "/" + new_file


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    path = dir_str + "/" + filename
    if filename.startswith("_"):
        with open(path, "r") as f:
            data = f.read()
            data = json.loads(data)  # string to list
        with open(new_file_path, "a+") as f:
            f.write(str(my_filter(data)))
