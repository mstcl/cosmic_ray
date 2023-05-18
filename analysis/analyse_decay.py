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
from scipy.optimize import curve_fit


def fun(arr, size):
    shape = arr.shape[:-1] + (arr.shape[-1] - size + 1, size)
    strides = arr.strides + (arr.strides[-1],)
    return np.lib.stride_tricks.as_strided(arr, shape=shape, strides=strides)


from event import Event, Pulse

parser = argparse.ArgumentParser(description="Analyse CSV file")
parser.add_argument("-i", "--in_file", help="input file")
parser.add_argument("-o", "--out_file", help="output file")
parser.add_argument("-n", "--n_max", help="max number of lines to process")

args = parser.parse_args()

# open the file
ifile = open(args.in_file, "rb")
events = pickle.load(ifile, encoding="latin1")
n_events = len(events)
# pulse logic
copper_distribution = []
size1, size2, size3 = 0, 0, 0
event_ct = 0
for event in events:
    event_ct += 1
    pulse_chans = []
    for pulse in event.pulses:
        if pulse.edge == 0:
            pulse_chans.append(pulse.chan)

    # exclusively 0,1,2 or 1,2,3
    if pulse_chans == [0, 1, 2] or pulse_chans == [1, 2, 3]:
        count = 0
        for pulse in event.pulses:
            if pulse.edge != 0:
                continue
            if count == 0:
                time0 = pulse.time
            if count == 1:
                time1 = pulse.time
            if count == 2:
                time2 = pulse.time
            count += 1
        # if ((time2 - time0) > 40) and ((time1 - time0) <= 40):
        copper_distribution.append(np.abs(time2 - time1))
        size1 += 1

    # exclusively 0,1,2,3 or 0,1,2,2
    length = 4
    pulse_chans = np.array(pulse_chans)
    if np.size(pulse_chans) >= length:
        combs = [[0, 1, 2, 3], [0, 1, 2, 2]]
        for com in combs:
            inds = np.all(fun(pulse_chans, length) == com, axis=1)
            res = np.mgrid[0 : len(inds)][inds]
            if np.size(res) != 0:
                for val in res:
                    count = 0
                    for pulse in event.pulses:
                        if pulse.edge != 0:
                            continue
                        if count == val:
                            time0 = pulse.time
                        if count < val:
                            count += 1
                            continue
                        if count >= val + length:
                            break
                        if count == val + 2:
                            time2 = pulse.time
                        if count == val + 3:
                            time3 = pulse.time
                        count += 1
                    # if ((time3 - time0) > 40) and ((time2 - time0) <= 40) :
                    copper_distribution.append(np.abs(time3 - time2))
                    size2 += 1

    # exclusively 0,1,1 or 1,2,2
    length = 3
    if np.size(pulse_chans) >= length:
        combs = [[0, 1, 1], [1, 2, 2]]
        for com in combs:
            inds = np.all(fun(pulse_chans, length) == com, axis=1)
            res = np.mgrid[0 : len(inds)][inds]
            if np.size(res) != 0:
                for val in res:
                    count = 0
                    for pulse in event.pulses:
                        if pulse.edge != 0:
                            continue
                        if count == val:
                            time0 = pulse.time
                        if count < val:
                            count += 1
                            continue
                        if count >= val + length:
                            break
                        if count == val + 1:
                            time1 = pulse.time
                        if count == val + 2:
                            time2 = pulse.time
                        count += 1
                    # if ((time2 - time0) > 40) and ((time1 - time0) <= 40):
                    copper_distribution.append(np.abs(time2 - time1))
                    size3 += 1

    # if len(pulse_chans) == 4:
    #    time0, time1, time2, time3 = 0, 0, 0, 0
    #    if pulse_chans == [0,1,2,3]:
    #        for pulse in event.pulses:
    #            if pulse.edge == 0 and pulse.chan == 0:
    #                time0 = pulse.time
    #            if pulse.edge == 0 and pulse.chan == 1:
    #                time1 = pulse.time
    #            if pulse.edge == 0 and pulse.chan == 2:
    #                time2 = pulse.time
    #            if pulse.edge == 0 and pulse.chan == 3:
    #                time3 = pulse.time
    #        copper_distribution.append(np.abs(time3-time2))
    #    if pulse_chans == [0,1,2,2]:
    #        for pulse in event.pulses:
    #            if pulse.edge == 0 and pulse.chan == 0:
    #                time0 = pulse.time
    #            if pulse.edge == 0 and pulse.chan == 1:
    #                time1 = pulse.time
    #            if pulse.edge == 0 and pulse.chan == 2:
    #                if time2 == 0:
    #                    time2 = pulse.time
    #                else:
    #                    time3 = pulse.time
    #        copper_distribution.append(np.abs(time3-time2))
    # if len(pulse_chans) == 3:
    # time0, time1, time2 = 0, 0, 0

print(size1, size2, size3)
print("total size", np.size(copper_distribution))
print("total events", event_ct)
copper_distribution = np.array(copper_distribution)
copper_distribution = copper_distribution[copper_distribution != 0]
# plt.scatter(
    # np.arange(0, np.size(copper_distribution), 1), copper_distribution, color="r"
# )
# plt.ylabel("time difference (muon stopped - electron hit) (ns)")
# plt.xlabel("index")
# plt.show()


def fit(t, A, B, tau):
    return A + B * np.exp(-t / tau)


# nums = np.linspace(300, 1600, 20, dtype=np.int_)
# # nums2 = np.linspace(1800,2100,20, dtype=np.int_)
# taus = np.zeros_like(nums, dtype=np.float_)
# tau_errors = np.zeros_like(nums, dtype=np.float_)
# bin_widths = np.zeros_like(nums, dtype=np.float_)
# for idx, val in enumerate(nums):
bins = np.linspace(2.,1000., 500)
# print(val)
# bins = np.logspace(np.log(0.1),np.log(1.0),75)
bin_heights, bin_borders, _ = plt.hist(
    copper_distribution, bins=bins, label="histogram"
)
bin_centers = bin_borders[:-1] + np.diff(bin_borders) / 2
popt, pcov = curve_fit(fit, bin_centers, bin_heights, p0=[1.0, 0.0, 1.0])
x_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 10000)
plt.plot(x_interval_for_fit, fit(x_interval_for_fit, *popt), label="fit")
plt.legend()
# plt.yscale("log", base=np.e)
# plt.yticks(np.array([1, np.e, 2*np.e]),['1','2.718'])
plt.ylabel("N")
plt.xlabel(r"$\Delta t$")
plt.show()

# bin_widths[idx] = (bin_borders[1] - bin_borders[0])
y_err = np.sqrt(bin_heights)
t_err = (bin_borders[1] - bin_borders[0]) / 2
A, B, tau = popt
A_err, B_err, tau_err = np.sqrt(np.diag(pcov))

log_values = np.log(np.abs(bin_heights - A) / B)
tau_err_prop = tau * np.sqrt(
    (t_err / log_values) ** (2)
    + (t_err * (log_values) * (-2))
    * (
        (y_err / (bin_heights - A)) ** (2)
        + (A_err / (bin_heights - A)) ** (2)
        + (B_err / B) ** (2)
    )
)
tau_err_total = np.mean(tau_err_prop + tau_err)
# taus[idx] = tau
# tau_errors[idx] = tau_err_total

print(tau,np.mean(tau_err_prop + tau_err))
print(np.size(bin_heights))
# plt.cla()
# plt.clf()
# plt.close()
# plt.errorbar(nums, taus, yerr=tau_errors,capsize=1.0, marker='x', ls='', color="k")
# # plt.scatter(nums,bin_widths)
# plt.xlabel("Bin width (ns)")
# plt.ylabel(r"$\tau$ (ns)")
# plt.show()
