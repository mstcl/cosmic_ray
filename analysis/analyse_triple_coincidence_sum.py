#!/usr/bin/env python

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

ifile = open(args.in_file, 'rb')
events= pickle.load(ifile)
n_events= len(events)


def calculate_counts(trig_1, trig_2, trig_3, target_1):
'''
Function takes a baseline of three channels (trig_1, trig_2, trig_3) and the fourth channel as the "target" (target_1);
Computes triple coincidence in the baseline and quadruple coincidence for the baseline and target;
Returns the number of coincidences for the aforementioned values.
'''
    n_coinc = 0
    n_coinc_1 = 0
    for event in events:
        found0 = False
        found1 = False
        found2 = False
        found3 = False
        for pulse in event.pulses:
            if pulse.edge==0 and pulse.chan == int(trig_1):
                found0 = True
            if pulse.edge==0 and pulse.chan == int(trig_2):
                found1 = True
            if pulse.edge==0 and pulse.chan == int(trig_3):
                found2 = True
            if pulse.edge==0 and pulse.chan == int(target_1):
                found3 = True
        if found0 and found1 and found2:
            n_coinc += 1
        if found0 and found1 and found2 and found3:
            n_coinc_1 += 1
    return n_coinc, n_coinc_1

#opens text files in which the efficiencies will be stored
C0f=open("C0-eff-sum.txt","a")
C1f=open("C1-eff-sum.txt","a")
C2f=open("C2-eff-sum.txt","a")
C3f=open("C3-eff-sum.txt","a")

#obtains coincidence values for each permutation
#notation is as follows: c represents channel, and is followed by the channel's number; b at the end delegates the current baseline permutation; o represents the channel whose efficiency is being measured
c0c1c2b,c3o=calculate_counts(0,1,2,3)
c0c1c3b,c2o=calculate_counts(0,1,3,2)
c0c2c3b,c1o=calculate_counts(0,2,3,1)
c1c2c3b,c0o=calculate_counts(1,2,3,0)

print(c0o,c10,c20,c30)

#efficiencies for a particular run are appended to the opened files; the files are subsequently closed
C0f.writelines("{}\t{}\n".format(c1c2c3b,c0o))
C0f.close()

C1f.writelines("{}\t{}\n".format(c0c2c3b,c1o))
C1f.close()

C2f.writelines("{}\t{}\n".format(c0c1c3b,c2o))
C2f.close()

C3f.writelines("{}\t{}\n".format(c0c1c2b,c3o))
C3f.close()

