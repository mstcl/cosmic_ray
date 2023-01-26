#!/bin/sh

# example script for automating several data taking runs
# Usage :
#  bash run_all.sh
#
i=0
n=50
while [ $i -ne 4 ]
do
    while [ $n -ne 1010 ]
    do
        acquire.py -t 100 -o thresh100_${i}.txt -0 ${n} -e 0x$(dc -e "2 ${i} ^ p")
        n=$(($n+10))
    done
    i=$(($i+1))
done
