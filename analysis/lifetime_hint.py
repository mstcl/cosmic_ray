
# data analysis example program
# Including some examples of how to use DataFrames from pandas
#
# Usage :
# python analysis2.py -i test.csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

from scipy.stats import expon

import argparse
parser = argparse.ArgumentParser(description='Convert Quarknet to CSV')
parser.add_argument("-i", "--in_file", help="input file")
parser.add_argument("-o", "--out_file", help='output file')
parser.add_argument("-m", "--max_lines", help='maximum number of lines to process', default=1e9, type=int)

args = parser.parse_args()

# open the file
df = pd.read_csv(args.in_file)

# the event variables store information about the "current" event
current_event = 0
pulses = []
start_time = 0.
end_time = 0.
isStopped = False
isDownwardsDecay = False
isUpwardsDecay = False

# these variables are the output of the loop
n_stopped = 0
n_downwards_decay = 0
n_upwards_decay = 0
decay_times = []


# loop over lines
for index, row in df.iterrows():

    if (index<args.start_line):
        
        
    if (index>args.max_lines):
        break

    # do this when there is a new event
    if (not row['event_id']==current_event):
    
        # first sort pulses by time
        pulses.sort(key=lambda tup: tup["time"])

        # get time of the first pulse
        if len(pulses)==0:
            start_time = pulses[0]["time"]


        ### now decide whether an event is a stopped muon, whether it decays, and time of the decay 
        ### the 'pulses' variable is a list of rising edge pulses in this event, sorted by time
        ### you can loop over them using 'for pulse in pulses:' and then 
        ### pulse["chan"] will give the channel of the pulse
        ### pulse["time"] will give the time of the pulse (remember to subtract the start time !)
            
        
        # count stopped muons
        if isStopped:
            n_stopped = n_stopped + 1
        
        # reset the event variables
        pulses = []
        start_time = 0.
        end_time = 0.
        isStopped = False
        isDownwardsDecay = False
        isUpwardsDecay = False
        current_event = row['event_id']

    # store a tuple of pulse channels/times
    if (row['edge']==0):
        pulses.append({"chan":int(row['channel']) , "time":row['time']})


# print some information
print("N lines : ", index)
print("N stopped muons : ", n_stopped)
print("N downwards decays : ", n_downwards_decay)
print("N upwards decays : ", n_downwards_decay)

### now do some analysis of the results of the loop ###
