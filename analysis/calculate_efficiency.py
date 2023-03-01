#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

def c1():
    labels = [[(4,5),(4,8),(5,8)],[(1,5),(1,8),(5,8)],[(1,4),(1,8),(4,8)],[(1,4),(1,5),(4,5)]]
    tubes = [1,4,5,8]
    chans = [0,1,2,3]
    for chan, idx in enumerate(chans):
        with open("C{}-eff.txt".format(chan), "r") as data:
            tab = np.array([list(map(float,line.strip("\n").split("\t"))) for line in data.readlines()])
            print "Saving channel", chan
            tab = tab.T
            plt.scatter(np.array([n+1 for n in range(np.size(tab[0]))]), tab[0], label="baseline {}".format(labels[idx][0]), s=1)
            plt.scatter(np.array([n+1 for n in range(np.size(tab[1]))]), tab[1], label="baseline {}".format(labels[idx][1]), s=1)
            plt.scatter(np.array([n+1 for n in range(np.size(tab[2]))]), tab[2], label="baseline {}".format(labels[idx][2]), s=1)
            plt.legend()
            plt.ylabel("Efficiency")
            plt.xlabel("Run ID")
            plt.title("T{} efficiency across all baselines".format(tubes[idx]))
            plt.savefig("{}.png".format(tubes[idx]))
            plt.cla()
            plt.clf()
            plt.close()
            indiv_mean = np.mean(tab, axis=1)
            indiv_var = np.var(tab, axis=1)
            print "Average efficiency of each baseline for T{}".format(tubes[idx]), indiv_mean
            print "Variance of efficiency of each baseline for T{}".format(tubes[idx]), indiv_var


def c1_1():
    tubes = [1,4,5,8]
    chans = [0,1,2,3]
    for chan, idx in enumerate(chans):
        with open("C{}.txt".format(chan), "r") as data:
            tab = np.array([list(map(float,line.strip("\n").split("\t"))) for line in data.readlines()])
            tab = tab.T
            sum_X = np.sum(tab[:-1])
            sum_n = np.sum(tab[-1])
            print(sum_X, sum_n) 
            print("Average efficiency of each baseline for T{}".format(tubes[idx]), float(sum_X)/float(sum_n))


def c2():
    tubes = [1,4,5,8]
    chans = [0,1,2,3]
    for chan, idx in enumerate(chans):
        with open("C{}-eff-2.txt".format(chan), "r") as data:
            tab = np.array([list(map(float,line.strip("\n").split("\t"))) for line in data.readlines()])
	    tab = tab.T
            indiv_mean = np.mean(tab)
            indiv_var = np.var(tab)
            plt.scatter(np.array([n+1 for n in range(np.size(tab))]), tab, s=1)
            plt.ylabel("Efficiency")
            plt.xlabel("Run ID")
            plt.title("T{} efficiency".format(tubes[idx]))
            #plt.savefig("{}.png".format(tubes[idx]))
	    plt.show()
            plt.cla()
            plt.clf()
            plt.close()
            print "Average efficiency of each baseline for T{}".format(tubes[idx]), indiv_mean
            print "Variance of each baseline for T{}".format(tubes[idx]), indiv_var
   

def c2_2():
    tubes = [1,4,5,8]
    chans = [0,1,2,3]
    for chan, idx in enumerate(chans):
        with open("C{}-eff.txt".format(chan), "r") as data:
            tab = np.array([list(map(float,line.strip("\n").split("\t"))) for line in data.readlines()])
            print "Saving channel", chan
            tab = tab.T
            plt.errorbar(np.array([n+1 for n in range(np.size(tab[0]))]), tab[0], yerr=tab[1])
            plt.legend()
            plt.ylabel("Efficiency")
            plt.xlabel("Run ID")
            plt.title("T{} efficiency".format(tubes[idx]))
            plt.savefig("{}.png".format(tubes[idx]))
            plt.cla()
            plt.clf()
            plt.close()
            indiv_mean = np.mean(tab[0])
            indiv_var = np.mean(tab[[1])
            print "Average efficiency for T{}".format(tubes[idx]), indiv_mean
            print "Average error in efficiency for T{}".format(tubes[idx]), indiv_var


if __name__ == "__main__":
    c2()
