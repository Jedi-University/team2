#!/bin/bash
count_lines=$1

echo "Run 1: grouped"
head -n $count_lines clicks.txt | python mr_grouped.py -r local > grouped.txt 
echo "Run 2: location"
python mr_location.py -r local grouped.txt > location.txt
echo "Run 3: timestamp"
head -n $count_lines clicks.txt | python mr_timestamp.py -r local > time_location.txt