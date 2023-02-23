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
			print("Saving channel", chan)
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
			print("Average efficiency of each baseline for T{}".format(tubes[idx]), np.mean(tab, axis=1))
			print("Average efficiency across all baselines for T{}".format(tubes[idx]), np.mean(tab))
			

if __name__ == "__main__":
	c1()
