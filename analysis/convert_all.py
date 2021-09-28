#!/usr/bin/python

import os
import glob

pwd = os.environ.get('PWD')
crbase = os.environ.get('CR_BASE')
files = glob.glob(pwd+"/*.txt")

for file in files:
    if file.endswith(".txt"):
        outfile = file[:-4]+".pkl"
        cmd = crbase+"/analysis/convert.py -i "+file+" -o "+outfile
        print(cmd)
        os.system(cmd)


