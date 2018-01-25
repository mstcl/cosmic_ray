
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

# define early and late pulses
time_cut = 120.


# these variables store information about the "current" event
current_event = 0
start_time = 0.
end_time = 0.
channels_early = [False, False, False, False]
channels_late = [False, False, False, False]

# these variables are the output of the loop
n_cosmics = 0
n_stopped = 0
n_downwards_decay = 0
decay_times = []

# helper functions
def isStopped():
    return (channels_early[0] and channels_early[1]) and not (channels_early[2] or channels_early[3])

def isUpwards_decay():
    return (channels_late[0] or channels_late[1]) and not (channels_late[2] or channels_late[3])

def isDownwards_decay():
    return (channels_late[2] or channels_late[3]) and not (channels_late[0] or channels_late[1])


# loop over lines
for index, row in df.iterrows():

    if (index>args.max_lines):
        break

    # do this when there is a new event
    if (not row['event_id']==current_event):
        
        # check if this is a stopped muon, and if it decays downwards
        stopped = isStopped()
        downwards_decay = isDownwards_decay()

        # count stopped muons
        if stopped:
            n_stopped = n_stopped + 1

        # for stopped muons with downwards decays, calculate and store the decay time
        if stopped and downwards_decay:
            n_downwards_decay = n_downwards_decay + 1
            decay_time = end_time - start_time
            decay_times.append(decay_time)
        
        # reset variables
        channels_early = [ False, False, False, False ]
        channels_late = [ False, False, False, False ]
        start_time = 0.
        end_time = 0.
        current_event = row['event_id']

    # check if this is an 'early' pulse
    if (row['edge']==0 and (row['time'])<time_cut):
        channels_early[ int(row['channel']) ] = True
        if (row['channel']==0 or row['channel']==1):
             start_time = row['time']

    # check if this is a 'late' pulse
    if row['edge']==0 and (row['time']>time_cut):
        channels_late[ int(row['channel']) ] = True
        if (row['channel']==2 or row['channel']==3):
            end_time = row['time']

# print some information
print("N lines : ", index)
print("N stopped muons : ", n_stopped)
print("N downwards decays : ", n_downwards_decay)
print("Mean decay time : ", np.mean(decay_times))

print(decay_times)

# fit to the histogram and print results
(loc, mu) = expon.fit(decay_times)
print ("Fit norm : ", loc)
print ("Fit mean : ", mu)

# make a histogram of decay times
bins = np.arange(0., 10000., 100.)
plt.hist(decay_times, bins)

# plot the fit
pdf_fitted =  expon.pdf(bins, loc=loc, scale=mu)
plt.plot(bins, pdf_fitted, 'r-')

# set log scale and label axes
#plt.yscale('log')
plt.xlabel('time (ns)')
plt.ylabel('counts')
#axes = plt.gca()
#axes.set_ylim([0.0, 15.0])

# save and show the plot
plt.savefig("decay_times.png")
plt.show()



