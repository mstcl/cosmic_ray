# classes to store cosmic ray experiment data

class Event(object):
        
    def __init__(self, id):
        self.id      = id
        self.trigger = 0
        self.pulses  = []

class Pulse(object):
    def __init__(self, chan, edge, time):
        self.chan    = chan
        self.edge    = edge
        self.time    = time

