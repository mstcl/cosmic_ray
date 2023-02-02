#!/opt/anaconda/bin/python

# data analysis example program
# Including some examples of how to use DataFrames from pandas
#
# Usage :
# python analysis.py -i test.dat

import pickle
import numpy as np
import matplotlib.pyplot as plt
import argparse

from event import Event, Pulse

parser = argparse.ArgumentParser(description='Analyse CSV file')
parser.add_argument("-i", "--in_file", help="input file")
parser.add_argument("-o", "--out_file", help='output file')
parser.add_argument("-n", "--n_max", help='max number of lines to process')

args = parser.parse_args()

# open the file
ifile = open(args.in_file, 'rb')
events= pickle.load(ifile)
n_events= len(events)

volt, channel = tuple(map(int,args.in_file[6:-4].split("_")))

# example event loop
count = [0, 0, 0, 0]  # counts per channel

for event in events:
    for pulse in event.pulses:
        # only count rising edges
        if pulse.edge == 0:
            count[pulse.chan] += 1


with open("{}.txt".format(channel), "a") as data:
    data.writelines("{}\t{}\n".format(volt, count[channel]))
