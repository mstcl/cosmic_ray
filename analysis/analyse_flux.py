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


def calculate_counts():
    quad_count = 0
    for event in events:
        found0 = False
        found1 = False
        found2 = False
        found3 = False
        for pulse in event.pulses:
            if pulse.edge==0 and pulse.chan == int(0):
                found0 = True
            if pulse.edge==0 and pulse.chan == int(1):
                found1 = True
            if pulse.edge==0 and pulse.chan == int(2):
                found2 = True
            if pulse.edge==0 and pulse.chan == int(3):
                found3 = True
        if found0 and found1 and found2 and found3:
            quad += 1
    return quad_count


effic = np.array([0.390, 0.785, 0.932, 0.293])
effic_err = np.array([0.006, 0.007, 0.005, 0.005])
theta = 0.9890
theta_err = 0.0006
flux_mu = 3*calculate_counts()/(np.prod(effic)*518400*np.pi*(1-(np.cos(0.989))**3))
flux_mu_err = flux_mu*np.sqrt((effic_err/effic)**2 + (3*np.sin(theta)*theta_err*(np.cos(theta))**2)/(1-(np.cos(theta))**3)**2)
