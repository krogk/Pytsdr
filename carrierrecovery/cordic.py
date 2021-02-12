# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 10:30:15 2021

@author: Kamil
"""

import numpy as np 


"""
Cordic Algorithm 
This function demonstrates operation of digital clock, esentially simulating
Voltage Controlled Oscillator (VCO)
Inputs:
    carrierFreq:   Normalised Carrier Frequency
    bitPeriod:     Number of samples to be used for each bit representation
    b1Filt         Convolution FIR Filter coefficients to be used 
    
Outputs:
    vout:         Voltage oscilator waveform
    cout:         Clock waveform
    rout:         waveform 
    dout0:        Data waveform
"""
def CordicAlgorithm(carrierFreq, bitPeriod, b1):
    
    clk = ([1.0,0.0])
    fref = carrierFreq * (1. +0.02 * ( np.random.rand() - 0.5))
    pref = 2 * np.pi * np.random.rand()
    voltage = 0.0
    vout = np.array(voltage)
    cout = clk[0]
    rout = np.cos(pref)
     
    quadrature = np.empty(0)
    
    nTaps = len(b1)
    mixed = np.zeros(nTaps)

    for i in range(0,2000):
        mixed = np.append(mixed[1:], -clk[1] * np.cos(pref + 2 * np.pi * fref * i))
        
        # Calculate output of FIR low-pass filter which is going to be the voltage controlling oscilators
        voltage = np.sum(b1 * mixed)
        
        # Multiply the oscilating terms
        c = np.cos(2 * np.pi * carrierFreq * (1.0 + 0.05 * voltage))
        s = np.sin(2 * np.pi * carrierFreq * (1.0 + 0.05 * voltage))
        
        # Roll to the next clock period by matrix multiplication of the taps
        clk = np.matmul(np.array( [ [c, -s], [s,c] ] ), clk )
        
        # Save values for ploting
        vout = np.append(vout, voltage)
        cout = np.append(cout, clk[0])
        quadrature = np.append(quadrature, clk[1])
        rout = np.append(rout, np.cos(pref+2*np.pi*fref*i))
        
    return vout, cout, rout, quadrature