#!/bin/bash

mkdir output
time python3 jobs/preprocessing1.py $1 >output/temp01
time python3 jobs/preprocessing2.py $1 >output/temp02
time python3 jobs/aggr_ip_clicks.py output/temp02 >output/grouped.txt
time python3 jobs/aggr_loc_clicks.py output/temp02 >output/location.txt
time python3 jobs/time_clicks.py output/temp01 >output/time_location.txt
rm output/temp*