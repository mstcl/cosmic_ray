#!/bin/sh

# example script for automating several data taking runs
# Usage :
#  bash run_all.sh
#

acquire.py -t 100 -o thresh100.txt -0 100 -1 100 -2 100 -3 100
acquire.py -t 100 -o thresh200.txt -0 200 -1 200 -2 200 -3 200
acquire.py -t 100 -o thresh300.txt -0 300 -1 300 -2 300 -3 300
acquire.py -t 100 -o thresh400.txt -0 400 -1 400 -2 400 -3 400
acquire.py -t 100 -o thresh500.txt -0 500 -1 500 -2 500 -3 500
acquire.py -t 100 -o thresh600.txt -0 600 -1 600 -2 600 -3 600
