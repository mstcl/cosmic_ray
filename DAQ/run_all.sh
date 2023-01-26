#!/bin/sh

# example script for automating several data taking runs
# Usage :
#  bash run_all.sh
#
i=0
while [ $i -ne 4 ]
do
    acquire.py -t 100 -o thresh100_${i}.txt -0 100 -e 0x$(dc -e "2 ${i} ^ p")
    acquire.py -t 100 -o thresh200_${i}.txt -0 200 -e 0x$(dc -e "2 ${i} ^ p")
    acquire.py -t 100 -o thresh300_${i}.txt -0 300 -e 0x$(dc -e "2 ${i} ^ p")
    acquire.py -t 100 -o thresh400_${i}.txt -0 400 -e 0x$(dc -e "2 ${i} ^ p")
    acquire.py -t 100 -o thresh500_${i}.txt -0 500 -e 0x$(dc -e "2 ${i} ^ p")
    acquire.py -t 100 -o thresh600_${i}.txt -0 600 -e 0x$(dc -e "2 ${i} ^ p")
    acquire.py -t 100 -o thresh700_${i}.txt -0 700 -e 0x$(dc -e "2 ${i} ^ p")
    acquire.py -t 100 -o thresh800_${i}.txt -0 800 -e 0x$(dc -e "2 ${i} ^ p")
    acquire.py -t 100 -o thresh900_${i}.txt -0 900 -e 0x$(dc -e "2 ${i} ^ p")
    acquire.py -t 100 -o thresh1000_${i}.txt -0 1000 -e 0x$(dc -e "2 ${i} ^ p")
    i=$(($i+1))
done
