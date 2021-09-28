# CosmicRayExpt

## Quick setup :

```bash
git clone https://github.com/jimbrooke/CosmicRayExpt.git
cd CosmicRayExpt
source setup.sh
```

It is highly recommended that you create a separate subdirectories for each data collection task, to organise your data (and results).  For example : 
```bash
mkdir data
cd data
```

You will then be able to run the commands below from the 'data' directory, to collect data and analyse it 

## Data Acquisition code
Code to setup the Quarknet board and record data can be found under the DAQ folder.

### daq.py
This is a python library of routines to control the hardware and record data.  In principle, you should not need to modify any code in this library, although you are welcome to do so.

### main.py
This is an example program, that uses functions from daq.py to setup the Quarknet board, and record data, and provides a command line interface.  You can run it using :
```bash
acquire.py -t 10
```
Where the number after the ‘-t’ flag is the number of seconds to record data.  (If you do not supply the -t flag, the program will run forever, or until you press ctrl-C.  However, this more of operation is not recommended).  You can also enable different channels, set thresholds, coincidence requirements via the command line.  For more information, type
```bash
acquire.py -h
```

Note that you can set the output file by using the ‘–o’ option.  By default, the program will run continuously and write to a filename based on the timestamp.

It is also worth noting that the program can be run with the following command, which will leave the program running in the background, even after you log out.
```bash
nohup acquire.py >& log.txt &
```
(The “>& log.txt” notation sends any printout from daq.py to the file log.txt).

### daq.cfg
This is used by main.py (only) and contains default settings for all the parameters needed to setup the Quarknet board.  Parameters supplied via the command line flags will override these settings.  The configuration file looks like this :
```python
[communication]
port = /dev/ttyUSB0

[daq]
# Threshold for each channel in mV
thresh_ch0 = 1000
thresh_ch1 = 350
thresh_ch2 = 250
thresh_ch3 = 250

# which channels are enabled
enable = 0xf

# trigger coincidence (0 - singles, 1 - double, 2 - triple, 3 - quadruple)
coincidence = 0

# trigger coincidence window (in 10ns units)
gate = 4

# readout window (in 10ns units)
window = 10
```

The threshold fields should be self explanatory.  The ‘coincidence’ field sets how many channels are required to pulse in coincidence in order to readout (0 means 1-fold coincidence, 1 means 2-fold, etc.).  The ‘gate’ field is the time window in which coincidence is required, in units of 40ns.  Whenever the coincidence requirements are satisfied, data is recorded.  The ‘window’ field sets controls the period of data that is readout for each coincidence.  Finally, the ‘enable’ field is a hexadecimal digit that sets whether each channel is enabled, with one bit per channel.  (eg. 0xf all channels active, 0x1 enables channel 0, 0x5 enables channels 0 and 2, etc.).  See p33 of the Quarknet manual or more information on the readout board setup.

### run_all.sh
This is an example of one way to automate several runs with different settings.  Another way to do this is to write your own programs , and directly call routines from daq.py, changing parameters for each run.  You can use main.py as an example. 


## Analysis code

Analysis code is stored in the analysis folder

### convert.py
The first simply converts the Quarknet output file format to CSV (comma-separated value). To run this, use :
```bash
convert.py –i input_file.txt –o data.pkl 
```
Like the data acquisition program, in principle you should not need to make any changes to this program.

### convert_all.py
This will find all the .txt files in the current directory, and run the command above to convert them to .pkl files.
```bash
convert_all.py 
```

### analysis.py
An example analysis program is provided, that calculates the rate of events in each channel.  It also includes some example functions to select events of different types.  To run it, use :
```bash
analysis.py –i data.pkl
```

Note that this is an EXAMPLE program.  It is not recommended that you use this file for your analysis directly.  Better is to create a new file for each new analysis task.  You can either start from a blank slate, or copy analysis.py to a new file like this :
```bash
cp $CR_BASE/analysis/analysis.py myanalysis.py
```

Then edit myanalysis.py, before running it :
```bash
myanalysis.py -i data.pkl
```
