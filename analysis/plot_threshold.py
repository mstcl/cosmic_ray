#! /opt/anaconda/bin/python

import matplotlib.pyplot as plt
import numpy as np

channels = [0,1,2,3]
for channel in channels:
    with open("{}".format(channel), "r") as file:
        data = file.readlines()
        data = np.array([list(map(int,line.strip("\n").split())) for line in
        data]).T
        plt.errorbar(data[0], data[1], xerr=0, yerr=np.sqrt(data[1]), c="k",
        fmt="o", ms=2.5, capsize=2.0)
        plt.title("Channel {} pulse distribution by threshold voltage".format(channel))
        plt.ylabel("Pulse counts")
        plt.xlabel("Voltage (mV)")
        plt.savefig("{}.png".format(channel))
        plt.cla()
        plt.clf()

