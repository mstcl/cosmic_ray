#!/bin/sh

# example script for automating several data taking runs
# Usage :
#  bash run_all.sh
#
i=0 #current channel (starts at initial channel)
minv=10 #starting threshold value
maxv=2000 #final threshold value
f=3 #final channel
increment=10 #increment for threshold value
while [ $i -le $f ]
do
    n=$minv #starting value
    while [ $n -le $maxv ]
    do
        acquire.py -t 100 -o thresh${n}_${i}.txt -${i} ${n} -e 0x$(dc -e "2 ${i} ^ p")
        n=$(($n+$increment))
    done
    i=$(($i+1))
done
