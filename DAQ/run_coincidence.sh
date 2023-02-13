#!/bin/sh

# Modify daq.cfg within data directory as required

i=0           # iterator
f=500         # number of runs
length=500    # run time in seconds

while [ $i -le $f ]
do
    acquire.py -o t1458-c1-${i} -t ${length} -s "daq.cg"
    i=$((i+1))
done
