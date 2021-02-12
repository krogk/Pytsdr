# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 14:50:22 2021

@author: Kamil Rog
"""

import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from modulation.bask import ook
from modulation.bpsk import bpsk
from modulation.qpsk import qpsk

from carrierrecovery import cordic
from carrierrecovery import costas

from coding import differential


import numpy as np 
from matplotlib import pyplot as plt
from scipy import fft
from scipy import signal


"""
Convert a positive integer num into an m-bit bit vector
Inputs:
    num:  Number to be converted into binary array
    m:    Number of bits to be used for the representation
    
Outputs:
    Array of binary values  

"""
def BinArray(num, m):
    return np.array(list(np.binary_repr(num).zfill(m))).astype(np.bool)


def PlotTimeDomain(data,title):
    plt.figure()
    plt.plot(data)
    plt.title(title) 
    
def PlotFrequencySpectrum(data,title):
    plt.figure()
    plt.plot(np.abs(fft.fft(data)))
    plt.title(title) 
   
"""
Main Function:
    Firstly parses arguments that specifcy the modulation Scheme

"""    
if __name__ == "__main__":
 
    # Handle optional arguments
    import argparse
    # Create argument parser object
    parser = argparse.ArgumentParser()
    # Create optional arguments
    parser.add_argument('--BASK', default=False, action='store_true')
    parser.add_argument('--BPSK', default=False, action='store_true')
    parser.add_argument('--QPSK', default=False, action='store_true')
    parser.add_argument('--CORDIC', default=False, action='store_true')
    parser.add_argument('--COSTASBPSK', default=False, action='store_true')
    #parser.add_argument('--debug', default=False, action='store_true')
    # Create a namespace for the optional arguments
    args = parser.parse_args()
 
    # Define student number
    idNum = 2536572 # 0b = 00 10 01 10 10 11 01 00 01 11 11 00
    binTestVector = [0,0,1,0,0,1,1,0,1,0,1,1,0,1,0,0,0,1,1,1,1,1,0,0]
    # Define number of bits
    nBits = 24
    # Obtain binary representation for student number
    idNumBin = BinArray(idNum,nBits)
    txBin = idNumBin
    
    # Signal Properties
    # Define normalised carrier signal frequency (Must be < 0.5)
    fc = 0.125
    # Number of samples per bit
    bitPeriod = 16
    
    # FIR Filter Design
    nTaps = 64
    cuttOffFrequency = 0.1
    b1 = signal.firwin(nTaps, cuttOffFrequency)
    mixed = np.zeros(nTaps)
    w1, h1 = signal.freqz(b1)
    
    # # Plot FIR filter frequency response
    # plt.title("Digital filter frequency response")
    # plt.plot(w1/2/np.pi, 20*np.log10(np.abs(h1)))
    # plt.ylabel("Amplitude Response/dB")
    # plt.xlabel("Frequency/Sample Rate")
    # plt.grid()

    
    # Notes: Rx Data has been padded by (number of taps/2) to flush the filter
    # IMO: This approach is best as it is up to the Rx to decide on the filtering parameters used. 

    print("Unmodulated TX Data: ")
    print(txBin)

    # Modulate and demodulate signals using one of the specified schemes
    if ( args.BASK == True):
        print("USING BASK SCHEME!")
        txBASK = ook.ModulationBASK(txBin, bitPeriod, fc)
        PlotTimeDomain(txBASK,"Binary Amplitude Shift Keying - Tx Waveform")
        PlotFrequencySpectrum(txBASK,"Binary Amplitude Shift Keying - Frequency Spectrum")
        rxBASK, rxBin = ook.DemodulationBASK(txBASK, nBits, bitPeriod, b1, nTaps)
        PlotTimeDomain(rxBASK,"Binary Amplistude Shift Keying - Rx Waveform")
        print ("Rx Data:")
        print(rxBin)
            
    if (args.BPSK == True):
        print("USING BPSK SCHEME!")
        txBPSK = bpsk.ModulationBPSK(txBin, bitPeriod, fc)
        PlotTimeDomain(txBPSK,"Binary Phase Shift Keying - Tx Waveform")
        PlotFrequencySpectrum(txBPSK,"Binary Phase Shift Keying - Frequency Spectrum")
        rxBPSK, rxBin = bpsk.DemodulationBPSK(txBPSK, fc, nBits, bitPeriod, b1, nTaps)
        PlotTimeDomain(rxBPSK,"Binary Phase Shift Keying - Rx Waveform")
        print ("Rx Data:")
        print(rxBin)
            
    if (args.QPSK == True):
        print("USING QPSK SCHEME!")
        txQPSK = qpsk.ModulationQPSK(txBin, bitPeriod, fc)
        PlotTimeDomain(txQPSK,"Quadrature Phase Shift Keying - Tx Waveform")
        PlotFrequencySpectrum(txQPSK, "Quadrature Phase Shift Keying - Frequency Spectrum")
        iRxQPSK, qRxQPSK, rxBin = qpsk.DemodulationQPSK(txQPSK, fc, nBits, bitPeriod, b1, nTaps)
        PlotTimeDomain(iRxQPSK, "Quadrature Phase Shift Keying - Rx Waveform - I")
        PlotTimeDomain(qRxQPSK, "Quadrature Phase Shift Keying - Rx Waveform - Q")
        print ("Rx Data:")
        print(rxBin)
        
        
    if (args.CORDIC == True):
        print("CORDIC ALGORITHM DEMO!")
        

        
        fc = 1/32
        bitPeriod = 128
        # FIR Filter Design
        nTaps = 128
        cuttOffFrequency = 0.005
        b1 = signal.firwin(nTaps, cuttOffFrequency)
        mixed = np.zeros(nTaps)
        w1, h1 = signal.freqz(b1)
        mixed = np.zeros(nTaps)
        # Create discrete convolution filter by reversing FIR coefficients
        b1 = np.flip(b1)
        
        # Run Cordic Algorithm
        vout, cout, rout, quadrature = cordic.CordicAlgorithm(fc, bitPeriod, b1)

        # plt.figure()
        # plt.plot(vout, color = 'b')
        # plt.show()
        
        plt.figure()
        plt.plot(cout, color = 'b')
        plt.plot(quadrature, color = 'r')
        plt.show()
        
        # plt.figure()
        # plt.plot(cout, color = 'b')
        # plt.plot(rout, color = 'r')
        # plt.show()
        
        
    if (args.COSTASBPSK == True):
        print("USING COSTAS LOOP TO DEMODULATE BPSK SCHEME!") 
        
        preludeNBits = 16
        # Add random binary data to ensure time for clock to lock before data bits
        prelude = np.array(np.random.randint(2, size=preludeNBits), dtype="bool")
        txBin = np.append(prelude,txBin)
       
        fc = 1/32
        bitPeriod = 128
        # FIR Filter Design
        nTaps = 128
        cuttOffFrequency = 0.005
        b1 = signal.firwin(nTaps, cuttOffFrequency)
        mixed = np.zeros(nTaps)
        w1, h1 = signal.freqz(b1)
        mixed = np.zeros(nTaps)
        # Create discrete convolution filter by reversing FIR coefficients
        b1 = np.flip(b1)
        
        # Differnetial Encoding
        nBits = 24+1 # Add differential encoding bit 
        difEncoded = differential.DifferentialEncoder(txBin)
        
        # Modulate Signal using BPSK scheme
        txBPSK = bpsk.ModulationBPSK(difEncoded, bitPeriod, fc)
        
        vout, cout, rout, dout0 = costas.CostasLoopBPSK(txBPSK, fc, bitPeriod, prelude.size, nBits, b1)
        
        # Run Heaviside function to detect bits in the waveform
        rxBin = np.uint8([np.heaviside(dout0[(2*i+1)*bitPeriod//2+nTaps//2],0) for i in range(prelude.size+nBits)])
    
        # Differential Decoding
        rxBin = differential.DifferentialDecoder(rxBin)
        
        # Splice array to contain only data i.e cut off prelude data
        rxBin = rxBin[preludeNBits:]
        print("Decoded data:")
        print(rxBin)
         
        
        lockFlag = True
        for i in range(len(binTestVector)):
            if(binTestVector[i] != rxBin[i] ):
                print("Bit Error Detected at: " + str(i) )
                # If there is a bit error it means the oscilator has not locked to the signal
                lockFlag = False
        
        if(lockFlag):
            print("VCO Sucesfully locked to a signal!" )
        else:
            print("VCO Not locked to signal!" )
        
        plt.figure()
        plt.plot(vout, color = 'b')
        plt.show()
        
        plt.figure()
        plt.plot(cout, color = 'b')
        plt.plot(rout, color = 'r')
        plt.show()
        
        plt.figure()
        plt.plot(dout0, color = 'b')
        plt.show()
        

        
    # plt.show()
    # for i in range(len(binTestVector)):
    #     if(binTestVector[i] != rxBin[i] ):
    #         print("Bit Error Detected at: " + str(i) )
    