'''
 * Signals.py
 *
 *  Created on:     16.05.2018
 *  Last modified: 
 *  Author:         Andrew Jason Bishop
 *
 *  Signal class is a combination of samples and time line for
 * time discrete signals. The constructor method generates the
 * time line by giving the sample rate. It is based on numpy.
 *
 *  SignalPlotter class simplifies plotting Signal instances by
 * virtue of the pyplot.subplot2grid() method. It also takes a
 * keyword dictionary for parameters like colspan, markers, etc.
 * 
'''

import matplotlib.pyplot as plt
import numpy as np

class Signal:

    def __init__(self, _samples, _fs):

        self.samples           = _samples
        self.sampleRate        = _fs
        self.number_of_samples = _samples.size

        self.addTimeLine()


    def addTimeLine(self):

        samplingInterval = 1.0/self.sampleRate
        end = samplingInterval * self.number_of_samples

        self.timeLine = np.arange(0, end, samplingInterval)


    def getMaxTime(self):

        index_of_last_sample = self.number_of_samples - 1
        return self.timeLine[index_of_last_sample]


class SignalPlotter:

    def __init__(self, _dimensions):

        self.gridDimensions = _dimensions


    def plotSignal(self, _signal, _coords, _kwargs={}):

        ax = self.makeAxes(_coords, _kwargs)
        artists = self.plotToAxes(_signal, ax)

        return artists


    def makeAxes(self, _coords, _kwargs):

        ax = plt.subplot2grid( self.gridDimensions, _coords, **_kwargs)
        return ax


    def plotToAxes(self, _signal, _ax):

        artists = _ax.plot(_signal.timeLine, _signal.samples)
        return artists


'''EOF'''

