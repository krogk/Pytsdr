# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 14:50:24 2021

@author: Kamil Rog
"""

import numpy as np 
from scipy import signal


"""
Modulate a signal using Binary Amplitude Shift keying scheme
Inputs:
    data:       Array of binary data to be modulated
    bitPeriod:  Number of samples to be used for each bit representation
    fc:         Normalised Carrier Frequency 
    
Outputs:
    txModulated: Array containing modulated signal  

"""
def ModulationBASK(data, bitPeriod, fc):
    nBits = len(data)
    txModulated = np.empty(0)
    t = 0
    
    # For each bit
    for i in range(nBits):
        # For each sample in bit representation
        for j in range(bitPeriod):
            # Compute Amplitude
            txModulated = np.append(txModulated, data[i]*np.cos(2*np.pi*fc*t))
            # Increment Sample Counter
            t += 1
            
    return txModulated
    
            
"""
Demodulate a signal using Binary Amplitude Shift keying scheme,
This essentially simulates a envelope detector( diode followed by low-pass filter)
Inputs:
    txModulated:    Array of modulated data to be demodulated
    nBits:          Number of bits expected to Rx
    bitPeriod:      Number of samples to be used for each bit representation
    filt:           FIR Filter coefficients to be used 
    nTaps:          Number of FIR filter taps
    
Outputs:
    rxFiltered: Array containing demodulated and filtered signal   
    rxBin:      Decoded binary sequence

"""
def DemodulationBASK(txModulated, nBits, bitPeriod, b1Filt, nTaps):
    # Rectify(half-wave) the signal
    rxRecified = txModulated * np.heaviside(txModulated,0)
    # Low Pass Filtering
    rxFiltered = signal.lfilter(b1Filt,1,rxRecified)
    # Add pading to account for FIR delay to obtain correct bit stream
    rxFiltered = np.append(rxFiltered, np.empty(nTaps//2))
    
    # Decode demodulated signal into bits
    rxBin = np.empty(0)
    # For each bit 
    for i in range(0,nBits):
        # Move to the middle of the bit period
        t = (2*i+1) * bitPeriod//2 + nTaps//2
        # Decode bit using thershold
        rxBin = np.append(rxBin, rxFiltered[t] > 0.1)
    
    return rxFiltered, rxBin
    