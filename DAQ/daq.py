import serial
import sys
import time
import os
from datetime import datetime
import gzip
import bz2
import signal

    
class FileWriter(object):
    
    def __init__(self,path):
        if os.path.exists(path):
            raise ValueError('File %s already exists'%path)
        if path.endswith('.gz'):
            self.file = gzip.open(path,'w')
        elif path.endswith('.bz2'):
            self.file = bz2.BZ2File(path,'w')
        else:
            self.file = open(path,'w')
    
    def writeln(self, line):
        self.file.write(line)

def connect(serialPort="/dev/ttyUSB0"):

    try:
        port = serial.Serial(port=serialPort, baudrate=115200,
                             bytesize=8,parity='N',stopbits=1,
                             timeout=1,xonxoff=True)
    except serial.SerialException, e:
        print e.message
        sys.exit(1)
    print "Successfully connected to serial port"

    return port


def hardReset(port):
    port.write('RE\r')
    time.sleep(10)
    port.write('RB\r')

def reset(port):
    port.write('RB\r')  # reset board

def enableCounters(port):
    port.write('CE\r')

def disableCounters(port):
    port.write('CD\r')
    time.sleep(1)

def setupReadout(port, wt02, wc00, wc02, wc03):
    port.write('WT 01 00\r')
    port.write('WT 02 ' + hex(wt02)[2:] + '\r')
    port.write('WC 00 ' + hex(wc00)[2:] + '\r')
    port.write('WC 01 00\r')
    port.write('WC 02 ' + hex(wc02)[2:] + '\r')
    port.write('WC 03 ' + hex(wc03)[2:] + '\r')

def setThresholds(port, thresh):
    # set thresholds
    for i,value in enumerate(thresh):
        port.write('TL ' + str(i) + ' ' + str(value) + '\r')
        print 'TL ' + str(i) + ' ' + str(value) + '\r'

def diagnostics(port):
    port.write('DC\r')  # print setup in hex
    port.write('DT\r')  # print setup in hex
    port.write('DG\r')  # print GPS info
    port.write('DS\r')  # display scalers
    port.write('TH\r')  # print thermometer data
    port.write('BA\r')  # print barometer data
    port.write('TI\r')  # print timer data
    port.write('ST 3 5\r')  # status line (manual says always run this)
    port.write('SA 1\r')  # status line (manual says always run this)
    time.sleep(1)

def setup(port, thresh, enable, coinc, gate, window):
    
    # setup words to write to Quarknet
    wt02 = gate & 0xff
    wc00 = enable+(coinc<<4)
    wc02 = window & 0xff
    wc03 = (window & 0xff00)>>8

    # print the configuration
    print 'WT 01 00\r'
    print 'WT 02 ' + hex(wt02)[2:] + '\r'
    print 'WC 00 ' + hex(wc00)[2:] + '\r'
    print 'WC 01 00\r'
    print 'WC 02 ' + hex(wc02)[2:] + '\r'
    print 'WC 03 ' + hex(wc03)[2:] + '\r'
    
    # setup Quarknet
    print 'Configuring Quarknet board'

    reset(port)
    disableCounters(port)
    setupReadout(port, wt02, wc00, wc02, wc03)
    setThresholds(port, thresh)
    diagnostics(port)

    print 'Finished setting up'


def read(port, writer):
    while port.inWaiting(): # If there is input
        line = port.readline() # read from Quarkent
        writer.writeln(line)   # and write to output

def defaultFilename():
    now = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
    default_filename = 'daq_' + now + '.txt'
    return default_filename

def endrun(port, writer):
    disableCounters(port)
    diagnostics(port)
    read(port, writer)
    port.close()

def run(port, outfile=None, runtime=0):

    if (outfile==None):
        outfile = defaultFilename()

    # Declare signal handler
    def sigHandler(signum, frame):
        print 'Signal handler called with signal', signum
        endrun(port)
        exit()

    # And link SIGQUIT to it.
    signal.signal(signal.SIGINT, sigHandler)
    signal.signal(signal.SIGQUIT, sigHandler)

    # record data
    writer = FileWriter(outfile)

    read(port, writer)
    enableCounters(port)

    if (runtime==0):
        print "Going to run forever.  Hit ctrl-C to end"
        try: # Check for errors
            while True:
                read(port, writer)
                time.sleep(0.1)

        finally: # If an error
            print "Unknown error - ending run"
            disableCounters(port)
            endrun(port, writer)

    else:
        print "Going to run for ", runtime
        start = time.time()
        t = 0
        try: # Check for errors
            while (t<runtime):
                read(port, writer)
                time.sleep(0.1)
                t = time.time() - start

        finally:
            print "Ending run"
            disableCounters(port)
            endrun(port, writer)



