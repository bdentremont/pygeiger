#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes and functions to support plotting geiger counter data.
See geiger_read.py.

@author: brian
"""
import time, math, calendar
import matplotlib.pyplot as plt
import matplotlib as mpl
import pathlib

program_dir = pathlib.Path(__file__).parent.resolve()
list_path = str(program_dir) + "/source_list.txt"
tmpl_path = str(program_dir) + "/source_tmpl.txt"

mpl.rcParams['toolbar'] = 'None' 
maxct = 600.

def Make_FullScreen_Figure():
    "create a full screen figure, return axes"
    dpi=400
    fig,axes = plt.subplots(ncols=1,num='geiger', figsize=[1920/dpi,1080/dpi], dpi=dpi)
    fig.canvas.toolbar_visible = False
    fig.subplots_adjust(bottom=0.20)#,left=0.20)
    plt.get_current_fig_manager().full_screen_toggle()
    axes.margins(x=0.1)
    return axes

class GeigerPlot():
    def __init__(self, ax, frq = 3., hst = 100,logo_path=None):
        self.ax = ax
        self.n_events = int(hst/frq) + 1 #size of event queue
        self.frq = frq #frequency in seconds
        ax.clear()
        ax.set_xlabel('Time (s)')
        ax.set_xlim((-hst,0))
        ax.set_ylabel('Counts per minute')
        ax.set_ylim((0,maxct))
        #self._line, = ax.plot([0.],[0.],color='#015697')
        self._mark, = ax.plot([0.],[0.],color='#015697',linestyle="",marker=".")       
        if logo_path:
            img = plt.imread(logo_path)               
            plt.imshow(img,extent=[-hst,0,0,maxct],aspect='auto')
        plt.grid()
        self.txt = plt.text(-80,375,'text',fontsize=8)
        self.sourcelist = SourceList()
        ax.figure.show()
    def update(self,es):
        'accepts data in the form of geiger_util.EventStack object'
        self._mark.set_data( (es.ts,es.ct*60./float(self.frq)) )
        self.txt.set_text(self.sourcelist.description)
        self.ax.figure.canvas.draw()
        self.ax.figure.canvas.flush_events()
    def wait(self):
        'wait until the next plot interval'
        time.sleep(self.frq-time.time()%self.frq)

class Source():
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    def __init__(self,name,halflife_yr,install_cpm,install_date=None):
        self.name = name
        self.halflife_yr = float(halflife_yr)
        self.install_cpm = float(install_cpm)
        if install_date:
            self.install_date = calendar.timegm(time.strptime(install_date, Source.fmt))
        else:
            self.install_date = calendar.timegm(time.gmtime())
    @property
    def age(self):
        return (calendar.timegm(time.gmtime()) - self.install_date)/3600/24/365.2415
    @property
    def activity(self):
        return self.install_cpm*math.exp(-math.log(2)*self.age/self.halflife_yr)
    def __str__(self):
        date = time.strftime(Source.fmt, time.gmtime(self.install_date))
        return '{},{},{},{}'.format(self.name, self.halflife_yr,self.install_cpm,date)

class SourceList():
    def __init__(self):
        with open(list_path) as f:
            self.sl = [Source(*l.strip('\n').split(',')) for l in f.readlines()]
        with open(tmpl_path) as f:
            self.tmpl = f.read()
    @property
    def activities(self):
        return {s.name:s.activity for s in self.sl}
    @property
    def description(self):
        return self.tmpl.format(**self.activities)
