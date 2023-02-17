#!/bin/bash
touch C0-eff.txt
touch C1-eff.txt
touch C2-eff.txt
touch C3-eff.txt

for filename in $HOME/data/T1458-C1/*.dat
    do
        #note i have no idea what this command does, but i assume it makes sure the current file is not being considered
        [ -e "$filename" ] || continue
	echo Analysing ${!filename}
	analysis.py -i "$filename" 
    
done    
