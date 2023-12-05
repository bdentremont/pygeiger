#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read Geiger Counter and plot counts per minute for serial device
dumping one byte per count.

Brian d'Entremont
2022-03-17
"""
import time
import lib_geiger_util as gu
import lib_geiger_plot as gp

duration = 30
serial = '/dev/ttyUSB0'

halflives = {'Po-210':0.37886,'Sr-90':28.79,'Co-60':5.27}

print("Beginning count proceedure of newly installed sources.")
queue = gu.GeigerQueue(serial,size=10000)
slist = []
for name, halflife_yr in halflives.items():
  input("Turn wheel to {} and press Enter to continue...".format(name))
  print('  starting count for {} seconds, please wait ...'.format(duration))
  queue.drain()
  time.sleep(duration)
  cpm = queue.drain()*60/duration
  s = gp.Source(name,halflife_yr,cpm)
  print('  {} ct/min'.format(cpm))
  slist.append(s)

response = "yes"
try:
    slist_old = gp.SourceList().sl
    print('Your new count changes activities as follows:')
    for i in range(len(halflives)):
        name=slist[i].name
        a_new = slist[i].activity
        a_old = slist_old[i].activity
        change = (a_new-a_old)/a_old*100.
        print("  {}: {:+.2f}%".format(name,change))
    print("Do you want to you want to overwrite the saved sources with your new counts?")
    while True:
        response = input('  Type "yes" or "no" and press Enter:')
        if response.lower() in {"yes","no"}:
            break
except FileNotFoundError:
    pass

if response == "yes":
    with open("source_list.txt","w") as f:
        for s in slist:
            print(s,file=f)
    print('Source calibrations successfully set.')
