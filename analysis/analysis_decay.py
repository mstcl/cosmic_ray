#!/usr/bin/python

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
events= pickle.load(ifile, encoding='latin1')
n_events= len(events)

print("Read {} events from file".format(n_events))

# example event loop
count = [0, 0, 0, 0]  # counts per channel

for event in events:
    for pulse in event.pulses:
        # only count rising edges
        if pulse.edge == 0:
            count[pulse.chan] += 1

print("Counts by channel")
print("Channel 0 : {} ".format(count[0]))
print("Channel 1 : {} ".format(count[1]))
print("Channel 2 : {} ".format(count[2]))
print("Channel 3 : {} ".format(count[3]))

# pulse logic
copper_distribution = []
paddle_distribution = []
for event in events:
    # print("Event start")
    found0 = False
    found1 = False
    found2 = False
    found3 = False
    time0 = 0.
    time1 = 0.
    time2 = 0.
    time3 = 0.
    pulse_count = 0
    for pulse in event.pulses:
        # only count rising edges
        # print("Pulse start")
        if pulse.edge==0 and pulse.chan == 0:
            found0 = True
            time0 = pulse.time
            pulse_count += 1
            
    if not found0:
        continue

    for pulse in event.pulses:
        if pulse_count > 4:
            break
        if pulse.edge==0 and pulse.chan == 1 and found1 == False:
            found1 = True
            time1 = pulse.time
            pulse_count += 1
        if pulse.edge==0 and pulse.chan == 2:
            if pulse.time - time0 <= 40:
                found2 = True
                time2 = pulse.time
                pulse_count += 1
            else:
                found3 = True
                time3 = pulse.time
                pulse_count += 1
        if pulse.edge==0 and pulse.chan == 3:
            if pulse.time - time0 > 40:
                found3 = True
                time3 = pulse.time
            pulse_count += 1

    if found0 and found1 and found2 and found3:
            time_paddles = np.abs(time2-time0)
            time_copper = np.abs(time3-time2)
            copper_distribution.append(time_copper)

print(copper_distribution)
#copper_distribution = np.array(copper_distribution)
#paddle_distribution = np.array(paddle_distribution)

#plt.scatter(np.arange(0,np.size(copper_distribution),1), copper_distribution, color='r')
#plt.scatter(np.arange(0,np.size(paddle_distribution),1), paddle_distribution, color='b')
#plt.show()
