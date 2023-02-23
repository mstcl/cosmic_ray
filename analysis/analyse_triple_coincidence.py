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


def calculate_efficiency(trig_1, trig_2, trig_3, target_1):
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


def efficiency(baseline,together):
    baseline=float(baseline)
    together=float(together)
    eff=together/baseline
    return eff


C0f=open("C0-eff-2.txt","a")
C1f=open("C1-eff-2.txt","a")
C2f=open("C2-eff-2.txt","a")
C3f=open("C3-eff-2.txt","a")

c0c1c2b,c3o=calculate_efficiency(0,1,2,3)
c0c1c3b,c2o=calculate_efficiency(0,1,3,2)
c0c2c3b,c1o=calculate_efficiency(0,2,3,1)
c1c2c3b,c0o=calculate_efficiency(1,2,3,0)

C0f.writelines("{}\n".format(efficiency(c1c2c3b,c0o)))
C0f.close()

C1f.writelines("{}\n".format(efficiency(c0c2c3b,c1o)))
C1f.close()

C2f.writelines("{}\n".format(efficiency(c0c1c3b,c2o)))
C2f.close()

C3f.writelines("{}\n".format(efficiency(c0c1c2b,c3o)))
C3f.close()
