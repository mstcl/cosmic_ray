#!/bin/sh

# Modify daq.cfg within data directory as required

i=0           # iterator
f=500         # number of runs
length=500    # run time in seconds

while [ $i -le $f ]
do
    acquire.py -o "t1458-c1-${i}.txt" -t ${length} -s "daq.cfg"
    i=$((i+1))
done
