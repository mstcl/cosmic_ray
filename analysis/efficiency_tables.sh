#!/bin/bash
touch C0-eff-sum.txt
touch C1-eff-sum.txt
touch C2-eff-sum.txt
touch C3-eff-sum.txt

for filename in $HOME/data/T1458-C1/*.dat
    do
        #note i have no idea what this command does, but i assume it makes sure the current file is not being considered
        [ -e "$filename" ] || continue
	echo Analysing ${!filename}
	analysis_triple_coincidence_sum.py -i "$filename" 
    
done    
