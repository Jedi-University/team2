#!/bin/bash
echo "Run 1: grouped"
python mr_grouped.py -r local clicks.txt > grouped.txt
echo "Run 2: location"
python mr_location.py -r local grouped.txt > location.txt
echo "Run 3: timestamp"
python mr_timestamp.py -r local clicks.txt > time_location.txt