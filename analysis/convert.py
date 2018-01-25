#!/usr/bin/python
#
# Convert Quarknet output to .csv
#

import sys
import gzip
import bz2
import numpy as np
import pandas as pd

# constants
freq = 25.0e6
clock_LSB = 40.
tmc_LSB = clock_LSB/8.

first_count=0

# fucntion to skip header lines
def read_headers():
    for line, i in zip(f, range(n_header_lines)):
        if args.verbose:
            print(line)

# function to get trigger count
def trigger_count(fields):
    count = int(fields[0],16)
    if args.verbose:
        print ("Trigger counter: " , hex(count))
    # if (output < 0):
    #     print ("Neg count : ", output)
    return np.uint64(count)

# function to find if this pulse is the start of a new event
def new_trigger(fields):
    re0 = int(fields[1],16)
    if args.verbose:
        print("Rising edge 0 :" , hex(re0))
    return ( re0 & (1 <<7) ) != 0
    


# the main part of the program starts here
import argparse

parser = argparse.ArgumentParser(description='Convert Quarknet to CSV')
parser.add_argument("-i", "--in_file", help="input file")
parser.add_argument("-o", "--out_file", help='output file')
parser.add_argument("-v", "--verbose", help='verbose')

args = parser.parse_args()



# open file
f = open(args.in_file)

event_id = 0
event_start = 0
output_lines = []

for line in f:
    if args.verbose:
        print(line)
        print("Event : ", event_id)
        
    # split the line into tokens
    fields = line.rstrip(" \t\n\r").split()

    # check there are the correct number of tokens for a data line
    if len(fields) != 16:
        continue

    # get some information from the line
    new_trig = new_trigger(fields)

    if (event_id==0):
        event_start = trigger_count(fields)

    if (new_trig):
        event_id   = event_id + 1
        event_start = trigger_count(fields)

    count = trigger_count(fields) - event_start

    # loop over channels and edges
    for chan in range(4):
        for edge in range(2):
            # get corresponding data
            data = int(fields[1 + edge + 2*chan],16)
            
            # if this is a pulse, extract information from data
            if data & (1 << 5) != 0:
                time_coarse = count*clock_LSB
                time_fine   = (data & 31) * tmc_LSB
                if time_coarse < 0.:
                    print("Neg time coarse : ", time_coarse)
                if time_fine < 0.:
                    print("Neg time fine : ", time_fine)
                time = time_coarse + time_fine
                output = []
                output.extend([event_id])
                output.extend([chan])
                output.extend([edge])
                output.extend([time])
                output_lines.append(output)
                if args.verbose:
                    print("%i %i %i %10.12f"%(event_id, chan, edge, time))


df_columns=["event_id", "channel", "edge", "time"]
df = pd.DataFrame(data=output_lines,columns=df_columns)

df.to_csv(args.out_file, index=False)


