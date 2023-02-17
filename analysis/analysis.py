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

print("Starting analysis")

# open the file
ifile = open(args.in_file, 'rb')
events= pickle.load(ifile)
n_events= len(events)

# print("Read {} events from file".format(n_events))

# example event loop
# count = [0, 0, 0, 0]  # counts per channel

# for event in events:
#     for pulse in event.pulses:
#         # only count rising edges
#         if pulse.edge == 0:
#             count[pulse.chan] += 1
# 
# print("Counts by channel")
# print("Channel 0 : {} ".format(count[0]))
# print("Channel 1 : {} ".format(count[1]))
# print("Channel 2 : {} ".format(count[2]))
# print("Channel 3 : {} ".format(count[3]))

# now find concidences betwen two channels (0 and 1)
def calculate_efficiency(trig_1, trig_2, target_1, target_2):
    n_coinc = 0
    n_coinc_1 = 0
    n_coinc_2 = 0
    for event in events:
        found0 = False
        found1 = False
        found2 = False
        found3 = False
        for pulse in event.pulses:
            # only count rising edges
            if pulse.edge==0 and pulse.chan == int(trig_1):
                found0 = True
            if pulse.edge==0 and pulse.chan == int(trig_2):
                found1 = True
            if pulse.edge==0 and pulse.chan == int(target_1):
                found2 = True
            if pulse.edge==0 and pulse.chan == int(target_2):
                found3 = True
        if found0 and found1:
            n_coinc += 1
        if found0 and found1 and found2:
            n_coinc_1 += 1
        if found0 and found1 and found3:
            n_coinc_2 += 1
    return n_coinc, n_coinc_1, n_coinc_2

def efficiency(baseline,together):
    baseline=float(baseline)
    together=float(together)
    eff=together/baseline
    return eff

C0f=open("C0-eff.txt","a")
C1f=open("C1-eff.txt","a")
C2f=open("C2-eff.txt","a")
C3f=open("C3-eff.txt","a")

#NOTATION: obtained-o_baseline-b e.g. c1o_c2c3b
#NOTATION: coincidence-b e.g. c2c3b

c0c1b,c2o_c0c1b,c3o_c0c1b=calculate_efficiency(0,1,2,3)
c0c2b,c1o_c0c2b,c3o_c0c2b=calculate_efficiency(0,2,1,3)
c0c3b,c1o_c0c3b,c2o_c0c3b=calculate_efficiency(0,3,1,2)
c1c2b,c0o_c1c2b,c3o_c1c2b=calculate_efficiency(1,2,0,3)
c1c3b,c0o_c1c3b,c2o_c1c3b=calculate_efficiency(1,3,0,2)
c2c3b,c0o_c2c3b,c1o_c2c3b=calculate_efficiency(2,3,0,1)

#C0 baselines: 1,2  1,3  2,3
C0f.writelines("{}\t{}\t{}\n".format(efficiency(c1c2b,c0o_c1c2b),efficiency(c1c3b,c0o_c1c3b),efficiency(c2c3b,c0o_c2c3b)))
C0f.close()

#C1 baselines: 0,2  0,3  2,3
C1f.writelines("{}\t{}\t{}\n".format(efficiency(c0c2b,c1o_c0c2b),efficiency(c0c3b,c1o_c0c3b),efficiency(c2c3b,c1o_c2c3b)))
C1f.close()

#C2 baselines: 0,1  0,3  1,3
C2f.writelines("{}\t{}\t{}\n".format(efficiency(c0c1b,c2o_c0c1b),efficiency(c0c3b,c2o_c0c3b),efficiency(c1c3b,c2o_c1c3b)))
C2f.close()

#C3 baselines: 0,1  0,2  1,2
C3f.writelines("{}\t{}\t{}\n".format(efficiency(c0c1b,c3o_c0c1b),efficiency(c0c2b,c3o_c0c2b),efficiency(c1c2b,c3o_c1c2b)))
C3f.close()


  
#n_0_1, n_coinc_1, n_coinc_2 = calculate_efficiency(0,1,2,3)
#print("N (0,1) coincidences: {}".format(n_0_1))
#print("N (0,1,2) coincidences: {}".format(n_coinc_1))
#print("N (0,1,3) coincidences: {}".format(n_coinc_2))
#print("Efficiency of channel 2: {}".format(float(n_coinc_1)/float(n_0_1)))
#print("Efficiency of channel 3: {}".format(float(n_coinc_2)/float(n_0_1)))
#
#n_1_2, n_coinc_1, n_coinc_2 = calculate_efficiency(1,2,0,3)
#print("N (1,2) coincidences: {}".format(n_1_2))
#print("N (1,2,0) coincidences: {}".format(n_coinc_1))
#print("N (1,2,3) coincidences: {}".format(n_coinc_2))
#print("Efficiency of channel 0: {}".format(float(n_coinc_1)/float(n_1_2)))
#print("Efficiency of channel 3: {}".format(float(n_coinc_2)/float(n_1_2)))
#
#n_2_3, n_coinc_1, n_coinc_2 = calculate_efficiency(2,3,0,1)
#print("N (2,3) coincidences: {}".format(n_2_3))
#print("N (2,3,0) coincidences: {}".format(n_coinc_1))
#print("N (2,3,1) coincidences: {}".format(n_coinc_2))
#print("Efficiency of channel 0: {}".format(float(n_coinc_1)/float(n_2_3)))
#print("Efficiency of channel 1: {}".format(float(n_coinc_2)/float(n_2_3)))
#
#n_0_2, n_coinc_1, n_coinc_2 = calculate_efficiency(0,2,1,3)
#print("N (0,2) coincidences: {}".format(n_0_2))
#print("N (0,2,1) coincidences: {}".format(n_coinc_1))
#print("N (0,2,3) coincidences: {}".format(n_coinc_2))
#print("Efficiency of channel 1: {}".format(float(n_coinc_1)/float(n_0_2)))
#print("Efficiency of channel 3: {}".format(float(n_coinc_2)/float(n_0_2)))
#
#n_0_3, n_coinc_1, n_coinc_2 = calculate_efficiency(0,3,1,2)
#print("N (0,3) coincidences: {}".format(n_0_3))
#print("N (0,3,1) coincidences: {}".format(n_coinc_1))
#print("N (0,3,2) coincidences: {}".format(n_coinc_2))
#print("Efficiency of channel 1: {}".format(float(n_coinc_1)/float(n_0_3)))
#print("Efficiency of channel 2: {}".format(float(n_coinc_2)/float(n_0_3)))
#
#n_1_3, n_coinc_1, n_coinc_2 = calculate_efficiency(1,3,0,2)
#print("N (1,3) coincidences: {}".format(n_0_3))
#print("N (1,3,0) coincidences: {}".format(n_coinc_1))
#print("N (1,3,2) coincidences: {}".format(n_coinc_2))
#print("Efficiency of channel 0: {}".format(float(n_coinc_1)/float(n_1_3)))
#print("Efficiency of channel 2: {}".format(float(n_coinc_2)/float(n_1_3)))



# get some pulse time information
# dts = []
# for event in events:
#    found0 = False
#    found1 = False
#    time0 = 0.
#    time1 = 0.
#    for pulse in event.pulses:
#        # only count rising edges
#        if pulse.edge==0 and pulse.chan == 0:
#            found0 = True
#            time0 = pulse.time
#        if pulse.edge==0 and pulse.chan == 1:
#            found1 = True
#            time1 = pulse.time
#    if found0 and found1:
#        dts.append(abs(time1-time0))

# print some summary info
# print("Mean delta-t : {}".format(np.mean(dts)))
# print("Std dev delta-t : {}".format(np.std(dts)))
# 
# bins = np.linspace(0.,20., 100)
# plt.hist(dts, bins)
# plt.yscale('log')
# plt.ylabel("N")
# plt.xlabel(r'$\Delta t$')
# plt.show()

