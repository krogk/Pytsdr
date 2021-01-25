# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 14:50:26 2021

@author: Kamil Rog
"""

import numpy as np 
from scipy import signal

    
"""
Modulate a signal using Binary Phase Shift keying scheme
Inputs:
    data:       Array of binary data to be modulated
    bitPeriod:  Number of samples to be used for each bit representation
    fc:         Normalised Carrier Frequency
    
Outputs:
    txModulated: Array containing modulated signal  

"""
def ModulationBPSK(data, bitPeriod, fc):
    nBits = len(data)
    txModulated = np.empty(0)
    t = 0
    
    # For each bit
    for i in range(nBits):
        # For each sample in bit representation
        for j in range(bitPeriod):
            # Compute Amplitude
            txModulated = np.append(txModulated, (2*data[i]-1)*np.cos(2*np.pi*fc*t))
            # Increment Sample Counter
            t += 1
            
    return txModulated

"""
Demodulate a signal using Binary phase Shift keying scheme,
This essentially a mixer, multiplying the Rx Signal with a discrete carrier
cosine( 2pi * sample number * carrier freq) 
Inputs:
    txModulated:   Array of modulated data to be demodulated
    fc:            Normalised Carrier Frequency
    bitPeriod:     Number of samples to be used for each bit representation
    b1Filt:        FIR Filter coefficients to be used in filtering stage
    nTaps:         Number of taps FIR filter contain. 
    
Outputs:
    rxFiltered: Array containing demodulated and filtered signal   
    rxBin:      Decoded binary sequence

"""
def DemodulationBPSK(txModulated, fc, nBits, bitPeriod, b1Filt, nTaps):
    rxDemodulated = np.empty(0)
    t = 0
    # For each bit
    for i in range(nBits):
        # For each sample in bit representation
        for j in range(bitPeriod):
            # Demodulate the signal 
            rxDemodulated = np.append(rxDemodulated, txModulated[t] * np.cos(2*np.pi*fc*t))
            t += 1
    
    # Low Pass Filtering
    rxFiltered = signal.lfilter(b1Filt,1,rxDemodulated)
    # Add pading to account for FIR delay to obtain correct bit stream
    rxFiltered = np.append(rxFiltered, -np.ones(nTaps//2))
    
    # Decode demodulated signal into bits
    rxBin = np.empty(0)
    # For each bit 
    for i in range(0,nBits):
        # Move to the middle of the bit period
        t = (2*i+1) * bitPeriod//2 + nTaps//2
        # Decode bit 
        rxBin = np.append(rxBin, rxFiltered[t] > 0.0)
        #rx_bin[i] = np.heaviside(rx_lpf[i], 0)
    
    return rxFiltered, rxBin
