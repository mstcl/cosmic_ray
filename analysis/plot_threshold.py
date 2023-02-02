#! /opt/anaconda/bin/python

import matplotlib.pyplot as plt
import numpy as np

channels = [0,1,2,3]
for channel in channels:
    with open("{}.txt".format(channel), "r") as file:
        data = file.readlines()
        data = np.array([list(map(int,line.strip("\n").split())) for line in
        data]).T
        plt.scatter(data[0], data[1], c="k")
        plt.title("Channel {}".format(channel))
        plt.ylabel("Pulse counts")
        plt.xlabel("Threshold voltage (mV)")
        plt.savefig("{}.png".format(channel))
        plt.cla()
        plt.clf()

