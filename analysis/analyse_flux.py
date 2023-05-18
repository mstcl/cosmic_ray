#!/usr/bin/python

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

parser = argparse.ArgumentParser(description="Analyse CSV file")
parser.add_argument("-i", "--in_file", help="input file")
parser.add_argument("-o", "--out_file", help="output file")
parser.add_argument("-n", "--n_max", help="max number of lines to process")

args = parser.parse_args()

ifile = open(args.in_file, "rb")
events = pickle.load(ifile, encoding="latin1")
n_events = len(events)


# def calculate_counts():
#     quad_count = 0
#     for event in events:
#         found0 = False
#         found1 = False
#         found2 = False
#         found3 = False
#         for pulse in event.pulses:
#             if pulse.edge == 0 and pulse.chan == int(0):
#                 found0 = True
#             if pulse.edge == 0 and pulse.chan == int(1):
#                 found1 = True
#             if pulse.edge == 0 and pulse.chan == int(2):
#                 found2 = True
#             if pulse.edge == 0 and pulse.chan == int(3):
#                 found3 = True
#         if found0 and found1 and found2 and found3:
#             quad_count += 1
#     return quad_count


def get_counts(trig_1, trig_2, trig_3, target_1):
    """
    Function takes a baseline of three channels (trig_1, trig_2, trig_3) and the fourth channel as the "target" (target_1);
    Computes triple coincidence in the baseline and quadruple coincidence for the baseline and target;
    Returns the number of coincidences for the aforementioned values.
    """
    n_coinc = 0
    n_coinc_1 = 0
    for event in events:
        found0 = False
        found1 = False
        found2 = False
        found3 = False
        for pulse in event.pulses:
            if pulse.edge == 0 and pulse.chan == int(trig_1):
                found0 = True
            if pulse.edge == 0 and pulse.chan == int(trig_2):
                found1 = True
            if pulse.edge == 0 and pulse.chan == int(trig_3):
                found2 = True
            if pulse.edge == 0 and pulse.chan == int(target_1):
                found3 = True
        if found0 and found1 and found2:
            n_coinc += 1
        if found0 and found1 and found2 and found3:
            n_coinc_1 += 1
    return n_coinc, n_coinc_1


c0c1c2b, c3o = get_counts(0, 1, 2, 3)
c0c1c3b, c2o = get_counts(0, 1, 3, 2)
c0c2c3b, c1o = get_counts(0, 2, 3, 1)
c1c2c3b, c0o = get_counts(1, 2, 3, 0)

def calculate_counts(trip_sum, quad):
    return trip_sum - quad


trip_sum = c0c1c3b + c0c1c2b + c0c2c3b + c1c2c3b
effic = np.array([0.390, 0.785, 0.932, 0.293])
effic_err = np.array([0.006, 0.007, 0.005, 0.005])
time = 518400  # seconds
theta = 0.9890  # radians
theta_err = 0.0006  # radians
rate_no_eff = calculate_counts(trip_sum,c3o) / time
flux_mu = (
    3
    * calculate_counts(trip_sum,c3o)
    / (np.prod(effic) * time * np.pi * (1 - (np.cos(theta)) ** 3))
)
flux_mu_err = flux_mu * np.sqrt(
    np.sum((effic_err / effic) ** 2)
    + (
        (3 * np.sin(theta) * theta_err * (np.cos(theta)) ** 2)
        / (1 - (np.cos(theta)) ** 3) ** 2
    )
    ** 2
)
print("Flux:", flux_mu, "Flux error:", flux_mu_err)
print("Rate:", rate_no_eff)
