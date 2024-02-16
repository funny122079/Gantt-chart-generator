#!/usr/bin/env python
# pylint: disable=R0902, R0903, C0103
"""
Gantt.py is a simple class to render Gantt charts, as commonly used in
"""

import os
import json
import platform
from operator import sub

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from datetime import datetime
import math

# TeX support: on Linux assume TeX in /usr/bin, on OSX check for texlive
if (platform.system() == 'Darwin') and 'tex' in os.getenv("PATH"):
    LATEX = True
elif (platform.system() == 'Linux') and os.path.isfile('/usr/bin/latex'):
    LATEX = True
else:
    LATEX = False

# setup pyplot w/ tex support
if LATEX:
    rc('text', usetex=True)


class Package():
    """Encapsulation of a work package

    A work package is instantiated from a dictionary. It **has to have**
    a label, astart and an end. Optionally it may contain milestones
    and a color

    :arg str pkg: dictionary w/ package data name
    """
    def __init__(self, pkg):

        self.name = pkg['name']
        self.start = pkg['start']
        self.end = pkg['end']

        try:
            self.milestones = pkg['milestones']
        except KeyError:
            pass

        try:
            self.legend = pkg['legend']
        except KeyError:
            self.legend = None

def parse_time(time_str):
    hour = int(time_str.split(':')[0])
    minute = int(time_str.split(':')[1])

    decimal = minute / 60
    return float(hour) + decimal

def min_time(timeList):
    minTime = min(timeList)
    decimal = parse_time(minTime) % 1
    result = 0
    if decimal == 0:
        result = parse_time(minTime) - 1
    else:
        result = int(parse_time(minTime))

    return result

def max_time(startTimes, endTimes):
    maxTime = 0
    for i in range(len(endTimes)):
        startHour = parse_time(startTimes[i])
        endHour = parse_time(endTimes[i])
        
        if endHour < startHour:
            endHour += 24
        if maxTime < endHour:
            maxTime = endHour
    
    maxTime = math.ceil(maxTime) + 1

    duration = maxTime - min_time(startTimes)
    return int(duration)
    
class Gantt():
    DEFCOLOR = "#01388f"
    """Gantt
    Class to render a simple Gantt chart, with optional milestones
    """
    def __init__(self, dataFile):
        """ Instantiation

        Create a new Gantt using the data in the file provided
        or the sample data that came along with the script

        :arg str dataFile: file holding Gantt data
        """
        self.dataFile = dataFile

        # some lists needed
        self.shifts = []
        self.names = []

        self._loadData()
        self._procData()

    def _loadData(self):
        """ Load data from a JSON file that has to have the keys:
            packages & title. Packages is an array of objects with
            a label, start and end property and optional milesstones
            and color specs.
        """

        # load data
        with open(self.dataFile) as fh:
            data = json.load(fh)

        # must-haves
        self.title = "Gantt Chart For Shifts"

        for pkg in data['shifts']:
            self.shifts.append(Package(pkg))

        self.names = [pkg['name'] for pkg in data['shifts']]

        self.xlabel = "time(Day)"

    def _procData(self):
        """ Process data to have all values needed for plotting
        """
        # parameters for bars
        self.nShifts = len(self.names)
        self.start = [None] * self.nShifts
        self.end = [None] * self.nShifts

        for pkg in self.shifts:
            idx = self.names.index(pkg.name)
            self.start[idx] = pkg.start
            self.end[idx] = pkg.end

        self.xticks = [float(i + min_time(self.start)) for i in range(max_time(self.start, self.end))]

        self.durations = []
        for i in range(self.nShifts):
            if (parse_time(self.end[i]) > parse_time(self.start[i])):
                duration = parse_time(self.end[i]) - parse_time(self.start[i])
            else: 
                duration = parse_time(self.end[i]) + 24 - parse_time(self.start[i])
            self.durations.append(duration)

        self.yPos = np.arange(self.nShifts, 0, -1)
        
        self.startDates = []
        for date in self.start:
            self.startDates.append(parse_time(date))

    def format(self):
        """ Format various aspect of the plot, such as labels,ticks, BBox
        :todo: Refactor to use a settings object
        """
        # format axis
        plt.tick_params(
            axis='both',    # format x and y
            which='both',   # major and minor ticks affected
            bottom='on',    # bottom edge ticks are on
            top='off',      # top, left and right edge ticks are off
            left='off',
            right='off')

        # tighten axis but give a little room from bar height
        plt.ylim(0.5, self.nShifts + .5)

        # add title and package names
        plt.yticks(self.yPos, self.names, ha='left', va='center')
        plt.tick_params(axis='y', pad=100)
        plt.title(self.title)

        if self.xlabel:
            plt.xlabel(self.xlabel)

        if self.xticks:
            xticksLabels = ["{}{}".format(int(i + min_time(self.start))%12 if int(i + min_time(self.start))%12 != 0 else 12, "A" if int(i + min_time(self.start)) % 24 < 12 else "P") for i in range(max_time(self.start, self.end))]
            plt.xticks(self.xticks, xticksLabels)

    def render(self):

        # init figure
        self.fig, self.ax = plt.subplots()
        self.ax.yaxis.grid(False)
        self.ax.xaxis.grid(True)

        colors = []
        for i in range(self.nShifts):
                colors.append(self.DEFCOLOR)

        self.barlist = plt.barh(self.yPos, self.durations,
                                left=self.startDates,
                                align='center',
                                height=.5,
                                alpha=1,
                                color=colors)
        
        for i in range(self.nShifts):
            text = self.names[i] +  ' | ' + self.start[i] + ' ~ ' + self.end[i]
            self.ax.text(self.startDates[i] + self.durations[i] / 2, self.yPos[i], text, va='center', ha='center', color='white', weight='bold')

        # format plot
        self.format()

    @staticmethod
    def show():
        """ Show the plot
        """
        plt.show()

    @staticmethod
    def save(saveFile='img/GANTT.png'):
        """ Save the plot to a file. It defaults to `img/GANTT.png`.

        :arg str saveFile: file to save to
        """
        plt.savefig(saveFile, bbox_inches='tight')


if __name__ == '__main__':
    g = Gantt('sample.json')
    g.render()
    g.show()
    g.save('img/GANTT.png')