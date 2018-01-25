#!/bin/sh

# example script for automating several data taking runs
# Usage :
#  bash run_all.sh
#

python daq.py -t 10 -c daq1.cfg -o daq_1_10.txt.gz
python daq.py -t 10 -c daq2.cfg -o daq_2_10.txt.gz
python daq.py -t 10 -c daq3.cfg -o daq_3_10.txt.gz
python daq.py -t 10 -c daq4.cfg -o daq_4_10.txt.gz
