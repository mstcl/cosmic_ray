import serial
import sys
import time
import os
from optparse import OptionParser
from datetime import datetime
from ConfigParser import ConfigParser
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

def printout():
    port.write('V1\r')  # print setup in readable form
    port.write('V2\r')  # print setup in readable form
    port.write('DC\r')  # print setup in hex
    port.write('DT\r')  # print setup in hex
    port.write('DG\r')  # print GPS info
    port.write('DS\r')  # display scalers
    port.write('TH\r')  # print thermometer data
    port.write('BA\r')  # print barometer data
    port.write('TI\r')  # print timer data
    port.write('ST 3 5\r')  # status line (manual says always run this)
    port.write('SA 1\r')  # status line (manual says always run this)


def main():
 
    # set output file name
    now = datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
    default_filename = 'daq_' + now + '.txt.gz'

    # read config file
    parser = OptionParser()
    parser.add_option('-o','--outfile',dest='outfile',
                       default=default_filename,help='Path of output file')
    parser.add_option('-c','--config',dest='cfgfile',
                       default='daq.cfg',help='Path of config file')
    parser.add_option('-t','--time',dest='time',
                       default=-1,help='Time to run in seconds')
    (options, args) = parser.parse_args(sys.argv[1:])
    
    config = ConfigParser()
    config.readfp(open(options.cfgfile))

    thresh_ch0 = config.getint('daq','thresh_ch0')
    thresh_ch1 = config.getint('daq','thresh_ch1')
    thresh_ch2 = config.getint('daq','thresh_ch2')
    thresh_ch3 = config.getint('daq','thresh_ch3')

    coinc = config.get('daq','coincidence')
    channels = config.get('daq','channels')
    wc00 = int(channels,0)+(int(coinc,0)<<4)

    gate = config.getint('daq','gate')
    gate0 = gate & 0xff
    gate1 = (gate & 0xff00)>>8

    serialPort = config.get('communication','port')


    # connect to Quarknet board
    try:
        port = serial.Serial(port=serialPort, baudrate=115200,
                             bytesize=8,parity='N',stopbits=1,
                             timeout=1,xonxoff=True)
    except serial.SerialException, e:
        print e.message
        sys.exit(1)
    print "Successfully connected to serial port"

    # print the configuration
    print 'WC 00 ' + hex(wc00)[2:] + '\r'
    print 'WC 01 00\r'
    print 'WC 02 ' + hex(gate0)[2:] + '\r'
    print 'WC 03 ' + hex(gate1)[2:] + '\r'
    
    # setup Quarknet
    print 'Configuring Quarknet board'
    
    port.write('RE\r')  # reset everything
    port.write('RB\r')  # reset board
    port.write('CD\r')  # disable counters during setup
    
    # set TMC delay
    port.write('WT 01 00\r') # TMC delay= 2 clockticks (48 ns)
    port.write('WT 02 02\r')

    # set coincidence 
    port.write('WC 00 ' + hex(wc00)[2:] + '\r')      # WC00 - coincidence/channels
    port.write('WC 01 00\r')
    port.write('WC 02 ' + hex(gate0)[2:] + '\r')
    port.write('WC 03 ' + hex(gate1)[2:] + '\r')

    # set thresholds
    for i,thresh in enumerate([thresh_ch0, thresh_ch1, thresh_ch2, thresh_ch3]):
        port.write('TL ' + str(i) + ' ' + str(thresh) + '\r')
        print 'TL ' + str(i) + ' ' + str(thresh) + '\r'
    
    # read back thresholds
    port.write('TL\r')
        
    port.write('CE\r')  # enable counters
    
    # print out some info
    printout()

    print 'Finished setting up, now recording data...'

    # Declare signal handler
    def sigHandler(signum, frame):
        print
        print 'Signal handler called with signal', signum
        port.close()

    # And link SIGQUIT to it.
    signal.signal(signal.SIGINT, sigHandler)
    signal.signal(signal.SIGQUIT, sigHandler)

    # record data
    writer = FileWriter(options.outfile)

    if (options.time<0):
        print "Going to run forever.  Hit ctrl-C to end"
        try: # Check for errors
            while True:
                while port.inWaiting(): # If there is input
                    line = port.readline() # read from Quarkent
                    writer.writeln(line)   # and write to output
                time.sleep(0.1)

        finally: # If an error ( or signal handler is hit )
            print "Quitting loop"
            printout() 

    else:
        print "Going to run for ", options.time
        start = time.time()
        trun = int(options.time)
        t = 0
        try: # Check for errors
            while (t<trun):
                while port.inWaiting(): # If there is input
                    line = port.readline() # read from Quarkent
                    writer.writeln(line)   # and write to output
                time.sleep(0.1)
                t = time.time() - start
            print "Ending run"
            printout()

        finally: # If an error ( or signal handler is hit )
            print "Quitting loop"
            printout()



if __name__ == '__main__':
    main()
