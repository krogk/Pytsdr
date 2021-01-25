# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 14:50:29 2021

@author: Kamil Rog
"""

import numpy as np 
from scipy import signal

 
"""
Modulate a signal using Quadrature Phase Shift keying scheme
Essentially simulate a bit splitter followed by PSK where:
    
in-phase arm is multiplied with cos(2*np.pi*fc*t)
quadrature arm arm is multiplied with -sin(2*np.pi*fc*t))
    
Inputs:
    data:       Array of binary data to be modulated
    bitPeriod:  Number of samples to be used for each bit representation
    fc:         Normalised Carrier Frequency
    
Outputs:
    txModulated: Array containing modulated signal  

"""
def ModulationQPSK(data, bitPeriod, fc):
    nBits = len(data) # This assumes the data set is even
    txModulated = np.empty(0)
    t = 0
    
    # For each symbol (bit pair)
    for i in range(0,int(nBits/2)):
        # For each sample in symbol representation
        iIndex = (i * 2)
        qIndex = (i * 2 + 1)
        for j in range(bitPeriod):
            # Compute Amplitude
            # Summation: I + Q 
            txModulated = np.append(txModulated, ((2*data[iIndex]-1)*np.cos(2*np.pi*fc*t)) + ((2*data[qIndex]-1)*np.sin(2*np.pi*fc*t)))
            # Increment Sample Counter
            t += 1
            
            
    print("txModulatedLen:" +str(len(txModulated)))
    return txModulated


"""
Demodulate a signal using Quadrature Phase Shift keying scheme,
This essentially a mixer, multiplying the Rx Signal with a discrete carrier:
    
in-phase arm is multiplied with cos(2*np.pi*fc*t)
quadrature arm arm is multiplied with -sin(2*np.pi*fc*t))
    
Then each waveform is filtered and decoded, finaly bit streams are
recombined
    
Inputs:
    txModulated:   Array of modulated data to be demodulated
    fc:            Normalised Carrier Frequency
    bitPeriod:     Number of samples to be used for each bit representation
    b1Filt:        FIR Filter coefficients to be used in filtering stage
    nTaps:         Number of taps FIR filter contain. 
    
Outputs:
    iFiltered: Array containing demodulated and filtered I signal
    qFiltered: Array containing demodulated and filtered Q signal
    rxBin:      Decoded binary sequence

"""
def DemodulationQPSK(txModulated, fc, nBits, bitPeriod, b1Filt, nTaps):
    iDemodulated = np.empty(0)
    qDemodulated = np.empty(0)
    t = 0
    # For each symbol (bit pair)
    for i in range(0,int(nBits/2)):
        # For each sample in symbol representation
        for j in range(bitPeriod):
            # Demodulate the signal 
            iDemodulated = np.append(iDemodulated, txModulated[t] * np.cos(2*np.pi*fc*t))
            qDemodulated = np.append(qDemodulated, txModulated[t] * np.sin(2*np.pi*fc*t))
            t += 1
    
    # Low Pass Filtering
    qFiltered = signal.lfilter(b1Filt,1,qDemodulated)
    iFiltered = signal.lfilter(b1Filt,1,iDemodulated)
    
    # Add pading to account for FIR delay to obtain correct bit stream
    iFiltered = np.append(iFiltered, -np.ones(nTaps//2))
    qFiltered = np.append(qFiltered, -np.ones(nTaps//2))
    
    # Decode demodulated signal into bits
    rxBin = np.empty(0)
    # For each bit 
    for i in range(0,int(nBits/2)):
        # Move to the middle of the bit period
        t = (2*i+1) * bitPeriod//2 + nTaps//2
        # Decode I and then Q bit
        rxBin = np.append(rxBin, iFiltered[t] > 0.0)
        rxBin = np.append(rxBin, qFiltered[t] > 0.0)
    
    return iFiltered, qFiltered, rxBin
    