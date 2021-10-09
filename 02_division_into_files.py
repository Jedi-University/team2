import sys
import pathlib

print("Dividing coin data into files:")

file_path = "coin_folder/ohlc.txt"
path = pathlib.Path(file_path)
if not path.exists():
    print("There is no such file or directory!")
    sys.exit()

with open(file_path, "r") as coin_data:
    data = coin_data.read()

data = data.split("],")
data = [d.replace("[", "") for d in data]
data[-1] = data[-1].replace("]", "")

num_of_entries = 30
temp = len(data) // num_of_entries
num_of_files = temp if len(data) % num_of_entries == 0 else temp + 1
for i in range(num_of_files):
    with open(str(path.parent) + f"/0{i + 1}_entry.txt", "w") as file:
        count = 0
        while count < num_of_entries:
            entry_number = i * num_of_entries + count
            if entry_number == len(data):
                break

            file.write(f"{data[entry_number]}\n")
            count += 1
        print(f"===> {entry_number}/{len(data)}")

print("Done!")
