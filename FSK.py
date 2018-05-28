'''
 * FSK.py
 *
 *  Created on:     01.03.2018
 *  Last modified:  
 *  Author:         Andrew Jason Bishop

 *  The classes FSK_modulator and FSK_demodulator help simulating
 * Frequency Shift Keying on time discrete signals. Especially in
 * finding the low limts of sample rates and symbol duration, all
 * relevant parameters can be varied.
 *
 *  Amplitude quantization is going to be supported soon, as well
 * as various demodulation stages and techniques.
 * 
'''

import matplotlib.pyplot as plt
import numpy as np

import Signals as sig

class FSK_modulator:

    def __init__(self, _fc, _fs, _T):

        self.carrierFreq    = _fc
        self.sampleRate     = _fs
        self.symbolDuration = _T
        self.baseBandSignal = None


    def set_modulation_parameters(self, _fc, _fs, _T):

        self.carrierFreq    = _fc
        self.sampleRate     = _fs
        self.symbolDuration = _T


    def generate_FSK_Signal(self, _symbolSequence, _modulationIndex, _phase=0.0):

        self.generate_BaseBandSignal( _symbolSequence)

        sineArguments = np.pi * self.baseBandSignal.timeLine * \
            ( 2 * self.carrierFreq + _modulationIndex / \
            self.symbolDuration * self.baseBandSignal.samples) + _phase
        FSK_samples = np.sin( sineArguments )

        FSK_signal = sig.Signal( FSK_samples, self.sampleRate )
        return FSK_signal


    def generate_BaseBandSignal(self, _symbolSequence):

        samples_per_symbol = self.symbolDuration * self.sampleRate
        baseBand_samples = np.repeat( _symbolSequence, samples_per_symbol )

        self.baseBandSignal = sig.Signal( baseBand_samples, self.sampleRate )


    def generate_basic_sines(self, _baseBandAmplitudes, _h):

        sines = []
        for amplitude in _baseBandAmplitudes:

            symbol = np.array([amplitude])
            sine = self.generate_FSK_Signal( symbol, _h )
            sines.append(sine)

        return sines


    def getBaseBandSignal(self):

        return self.baseBandSignal


class FSK_demodulator:

    def __init__(self, _symbols_as_FSK_signals):

        self.FSK_symbols = _symbols_as_FSK_signals
        self.xCorrSignals = []


    def xCorrStage(self, _fsk_signal):

        for symbol in self.FSK_symbols:

            xCorrSignal = self.correlate( _fsk_signal, symbol )
            self.xCorrSignals.append( xCorrSignal )


    def correlate(self, _fsk_signal, _symbol):

        fsk    = _fsk_signal.samples
        symbol = _symbol.samples
        xCorrResult = np.correlate( fsk, symbol )

        return self.samplesToSignal( xCorrResult, _fsk_signal.sampleRate )


    def samplesToSignal(self, _samples, _sampleRate):
        return sig.Signal( _samples, _sampleRate )


if __name__ == "__main__":


    fs = sampleRate      = 200e3  # example: fs = 44200; fc = 1700; n = 5
    fc = carrierFreq     = 20e3   # sampleRate/carrierFreq is nice to be be integer
    T  = symbolDuration  = 100e-6
    h  = modulationIndex = 2      # for wideband FSK h >> 1, for CPFSK narrowband 0.5<h<1.0
    ph = signalPhase     = 0.0    # phase in radiant

    # Baseband characteristics
    m=mark = 1; c=carrier = 0; s=space= -1
    symbolSeq          = np.array([ m, c, m, c, s, c, m, c, s, c, s, c, s, c, m, c ])
    baseBandAmplitudes = np.array([m, c, s])

    # Signal generation
    myModulator     = FSK_modulator( carrierFreq, sampleRate, symbolDuration )
    fsk_signal      = myModulator.generate_FSK_Signal( symbolSeq, modulationIndex )
    baseBand_signal = myModulator.getBaseBandSignal()
    fsk_sines       = myModulator.generate_basic_sines(baseBandAmplitudes , modulationIndex)

    # Recovering baseband signal (only cross correlation stage yet)
    myDemodulator   = FSK_demodulator( fsk_sines )
    myDemodulator.xCorrStage( fsk_signal )
    corr_mark       = myDemodulator.xCorrSignals[0]
    corr_space      = myDemodulator.xCorrSignals[1]

    # plots
    rows = 5; cols = 3
    mySignalPlotter = sig.SignalPlotter((rows,cols))

    mySignalPlotter.plotSignal(fsk_signal, (0,0), {'colspan':3, 'title':'FSK signal'})
    mySignalPlotter.plotSignal(baseBand_signal, (1,0), {'colspan':3, 'title':'base band signal'})
    mySignalPlotter.plotSignal(corr_mark,  (2,0), {'colspan':3, 'title':'xcorr of fsk and mark'})
    mySignalPlotter.plotSignal(corr_space, (3,0), {'colspan':3, 'title':'xcorr of fsk and space'})
    mySignalPlotter.plotSignal(fsk_sines[0], (rows-1,0), {'title':'mark'})
    mySignalPlotter.plotSignal(fsk_sines[1], (rows-1,1), {'title':'carrier'})
    mySignalPlotter.plotSignal(fsk_sines[2], (rows-1,2), {'title':'space'})

    plt.tight_layout()
    plt.show()


'''EOF'''

