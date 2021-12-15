import os
import csv

def digitizer(data):
    data_width=len(data[0])
    for i in data:
      for j in range(data_width):
        i[j]= (int(i[j]) if ("." not in i[j]) else float(i[j]))
        j=+1
    return data

def my_mean(data):  # incoming_array
    acc = 0
    for i in data:
        acc += i[4]
    return acc / float(len(data))


def my_filter(data):
    data=digitizer(data)
    acc = []
    for i in data:
        acc.append(i) if i[4] > my_mean(data) else None
    return acc


dir_str = "coin_folder"
directory = os.fsencode(dir_str)
new_file = "advanced_ohlc.txt"
new_file_path = dir_str + "/" + new_file

try:
    os.remove(new_file_path)
except OSError:
    pass

# os.remove(new_file_path)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    path = dir_str + "/" + filename
    if filename.startswith("_"):
        with open(path, "r",newline='') as f:
            # data = f.read()
            reader=csv.reader(f)
            data = list(reader)  # string to list
            filtered_data=my_filter(data)
        with open(new_file_path, "a+",newline='') as f:
            csv_out=csv.writer(f)
            csv_out.writerows(filtered_data[index] for index in range(len(filtered_data)))
