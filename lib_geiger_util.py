#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes and functions to support reading serial port geiger counter.

@author: brian
"""

import os
import time
import numpy as np
import serial
from threading import Thread
from queue import Queue, Empty

def enqueue_reads(port, q):
    "continually read bytes from port.read() to queue"
    while True:
        r = port.read(1)
        if r:
            q.put_nowait(r)
            
class GeigerQueue():
    def __init__(self, serial_dev=None, size = 1000):
        if serial_dev == None:
            import subprocess as sp
            popen = sp.Popen("./geiger_sim.py", stdout=sp.PIPE, universal_newlines=True)
            port = popen.stdout
        else:
            port = serial.Serial(
                port = serial_dev,
                baudrate = 9600, #128000
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 1
            )
        self._q = Queue(maxsize=size)
        self._t = Thread(target=enqueue_reads,args=(port,self._q))
        self._t.daemon = True #thread dies with program
        self._t.start()
    def drain(self):
        "remove all bytes from queue and return the count"
        try:
            n = 0
            while True:
                self._q.get_nowait()
                n += 1
        except Empty:
            pass
        return n

class EventStack():
    'Mantains a rolling log of event times and values'
    def __init__(self, size):
       self._ts = np.nan*np.empty(size) #times
       self._ct = np.nan*np.empty(size) #counts
       self._i = -1
       self._full = False
    def _wrap(self,series):
        if not self._full:
            return series[:self._i+1]
        return np.concatenate((series[self._i+1:], series[:self._i+1]))
    @property
    def n(self):
        'number of items stored'
        if self._full:
            return len(self._ts)
        return self._i+1
    @property
    def ts(self):
        'time series (s, backward from now)'
        return self._wrap(self._ts)-time.time()
    @property
    def ct(self):
        'counts'
        return self._wrap(self._ct)
    def smooth_ct(self, box_pts):
        if self.n <= box_pts:
            return self.ct
        box = np.ones(box_pts)/box_pts
        return np.convolve(self.ct, box, mode='same')
    def append(self,value): #append a value with current time
        self._i += 1
        if self._i > len(self._ct) - 1:
            self._i = 0
            self._full = True
        self._ts[self._i] = time.time()
        self._ct[self._i] = value

def local_path(name):
    "create a path to a file in the current script's directory"
    path = os.path.realpath(__file__)
    directory = os.path.split(path)[0]
    return os.path.join(directory,name)
