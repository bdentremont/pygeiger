#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read Geiger Counter and plot counts per minute for serial device
dumping one byte per count.

Requires python package: pyserial
Requires linux user to have access to serial device (dialout group)

Setup on Raspberian
	place files on the Desktop
	configure the user and packages
	  sudo adduser pi dialout
	  sudo apt-get install python3-serial python3-matplotlib

	set execution bit for both scripts:
	  chmod u+x /home/pi/Desktop/geiger_read.py /home/pi/Desktop/geiger_source_set.py
	On Raspberian to autorun at startup, add a line to the following file:
	  /home/pi/.config/lxsession/LXDE-pi
	with the content:
	  @lxterminal --command=/home/pi/Desktop/geiger_read.py

Brian d'Entremont
2023-08-24
"""

import lib_geiger_util as gu
import lib_geiger_plot as gp

axes = gp.Make_FullScreen_Figure()
gplot = gp.GeigerPlot(axes)
queue = gu.GeigerQueue('/dev/ttyUSB0')
evstack = gu.EventStack(gplot.n_events)

sl = gp.SourceList()

while True:
     gplot.wait()
     evstack.append(queue.drain())
     gplot.update(evstack)
    
