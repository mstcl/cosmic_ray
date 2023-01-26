#! /opt/anaconda/bin/python

import matplotlib.pyplot as plt
import numpy as np

with open("numbers_clean.txt", "r") as file:
    data = file.readlines()

data = [list(map(int,line.strip("\n").split())) for line in data]

data_transposed = np.array(data).T
threshold = data_transposed[0]
plt.scatter(threshold,data_transposed[1])
plt.show()
plt.scatter(threshold,data_transposed[2])
plt.show()
plt.scatter(threshold,data_transposed[3])
plt.show()
plt.scatter(threshold,data_transposed[4])
plt.show()

