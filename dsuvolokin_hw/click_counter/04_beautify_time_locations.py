# py 04_beautify_time_locations.py
import json

def lazy_line(filename):
    keep_reading = True
    while keep_reading:
        line = filename.readline()
        if line:
            yield line.split('\t')
        else:
            keep_reading = False

ml = {}
with open('pre_location.txt','r') as f:
    for s in lazy_line(f):
        hour = int(s[0].replace('\"',''))
        location = json.loads(s[1])
        if not ml.get(hour,False):
            ml[hour] = [location]
        else:
            ml[hour].append(location)


with open('location.txt','w') as f:
    f.write(json.dumps(ml))