#!/bin/sh

# example script for automating several data taking runs
# Usage :
#  bash run_all.sh
#
i=1
while [ $i -le 2 ]
do
    n=50
    while [ $n -le 1000 ]
    do
        acquire.py -t 100 -o thresh${n}_${i}.txt -0 ${n} -e 0x$(dc -e "2 ${i} ^ p")
        n=$(($n+100))
    done
    i=$(($i+1))
done
