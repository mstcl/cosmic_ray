#!/bin/sh

# example script for automating several data taking runs
# Usage :
#  bash run_all.sh
#
i=1
while [ $i -ne 4 ]
do
    n=50
    while [ $n -ne 1010 ]
    do
        acquire.py -t 100 -o thresh${n}_${i}.txt -0 ${n} -e 0x$(dc -e "2 ${i} ^ p")
        n=$(($n+10))
    done
    i=$(($i+1))
done
