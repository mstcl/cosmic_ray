
# data analysis example program
# Including some examples of how to use DataFrames from pandas
#
# Usage :
# python analysis2.py -i test.csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

import argparse
parser = argparse.ArgumentParser(description='Convert Quarknet to CSV')
parser.add_argument("-i", "--in_file", help="input file")
parser.add_argument("-o", "--out_file", help='output file')

args = parser.parse_args()

# open the file
df = pd.read_csv(args.in_file)

# iterate over the rows in the file, for example counting the number of rising edges in channel 0
n_edge = 0
for index, row in df.iterrows():
    if (row['channel']==0 and row['edge']==0):
        n_edge = n_edge + 1

print(n_edge)

# a more sophisticated way to do the same thing using DataFrame functions
n_edge2 = len(df.loc[(df['channel']==0) & (df['edge']==0)])
print(n_edge2)

# calculate the rate of rising edges in all channels and make a plot
time = 10.
channels = [0, 1, 2, 3]
rates = []
errors = []
for chan in channels:
    n = len(df.loc[(df['channel']==chan) & (df['edge']==0)])
    r = n/time
    er = math.sqrt(n)/time
    rates.append(r)
    errors.append(er)

plt.errorbar(channels,rates, yerr=errors, fmt='o')
plt.xlabel('channel #')
plt.ylabel('rate (Hz)')
axes = plt.gca()
axes.set_xlim([-0.1,3.1])

plt.savefig("rates.png")
#plt.show()

# clear the plot
plt.clf()


# example of how to handle events which cross multiple lines
# this example just counts the number of pulses in an event and outputs a list

# these variables store information about the "current" event
current_event = 0
n_pulses_current = 0
channels_current = []


# this variable stores the results from all events in a list
n_pulses = []
n_cosmics = 0
n_cosmics_pmt1 = 0

# loop over lines
for index, row in df.iterrows():

    # check if this is a new event (ie. the event_id changed since the last line)
    # if it is, store the current pulse count, reset the counter, and update the current event ID
    if (not row['event_id']==current_event):
        
        # first, store the stuff we want at the end of the loop
        n_pulses.append(n_pulses_current)
        
        # reset the "current event" variables
        n_pulses_current = 0
        channels_current = []
        
        # count cosmic muons
        if ((0 in channels) and (3 in channels)):
            n_cosmics = n_cosmics + 1
            if (1 in channels):
                n_cosmics_pmt1 = n_cosmics_pmt1 + 1
        
        # update the current event number
        current_event = row['event_id']
    
    # check if there is a rising edge and count them
    if (row['edge']==0):
        n_pulses_current = n_pulses_current + 1
        channels_current.append(row['channel'])
        
    
        
# for example, make a histogram of number of edges per event
plt.hist(n_pulses, bins=range(10))
axes = plt.gca()
axes.set_ylim([0.0, 15.0])
plt.savefig("edges_per_event.png")
plt.show()




