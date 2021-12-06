#!/bin/bash

time python3 jobs/job01.py $1 >output/temp01
time python3 jobs/job02.py $1 >output/temp02
time python3 jobs/job1.py output/temp02 >output/output1
time python3 jobs/job2.py output/temp02 >output/output2
time python3 jobs/job3.py output/temp01 >output/output3