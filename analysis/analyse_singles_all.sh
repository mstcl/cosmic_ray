#! /bin/sh

max=7
for i in `seq 2 $max`
do
    touch "${i}"
done

for f in *.dat
do
    analyse_singles.py -i "${f}"
done

plot_threshold.py
