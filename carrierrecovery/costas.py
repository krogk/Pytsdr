# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:51:03 2021

@author: Kamil
"""

import numpy as np 
from matplotlib import pyplot as plt
from scipy import signal

#from coding import differential


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
Costas Loop
Demodulate a signal using costas Loop and binary phase Shift keying scheme, 
Inputs:
    binString:     Binary String to be used
    carrierFreq:   Normalised Carrier Frequency
    bitPeriod:     Number of samples to be used for each bit representation
    nBits:         Number of bits expected to Rx
    b1             FIR Filter coefficients to be used 
    
    
Outputs:
    vout:         Voltage oscilator waveform
    cout:         Clock waveform
    rout:         waveform 
    dout0:        Data waveform
    

"""
def CostasLoop(binString, carrierFreq, bitPeriod, nBits, b1):

    clk = ([1.0,0.0])
    fref = carrierFreq * (1. +0.02 * ( np.random.rand() - 0.5))
    pref = 2 * np.pi * np.random.rand()
    voltage = 0.0
    vout = np.array(voltage)
    cout = clk[0]
    rout = np.cos(pref)
    dout0 = np.empty(0)

    nTaps = len(b1)
    mixed = np.zeros((2, nTaps))
    lpmixed = np.empty(2) 
    
    # For all bits in the Rx bit string including additional equal to amount of taps to flush the filter
    for i in range(0,bitPeriod*(prelude.size+nBits)+nTaps//2):
        
        # Modulation and demodulation in one step
        # Clock multiplied with (symbol value multiplied with the cosine clock)
        mixed[0,:] = np.append(mixed[0,1:], clk[0]  * (2 * binString[(i//bitPeriod) % (prelude.size+nBits)] -1) * np.cos(pref + 2 * np.pi * fref * i) ) 
        mixed[1,:] = np.append(mixed[1,1:], -clk[1] * (2 * binString[(i//bitPeriod) % (prelude.size+nBits)] -1) * np.cos(pref + 2 * np.pi * fref * i) ) 
        
        # Low Pass Filtering
        lpmixed = [np.sum(b1*mixed[j,:]) for j in range (2)]
        # Multiply the filter outputs at a mixer to obtain voltage
        voltage = lpmixed[0] * lpmixed[1]
        
        # Try to find appropraite value for alpha to obtain correct frequency
        c = np.cos(2 * np.pi * carrierFreq * (1.0 + 0.25 * voltage))
        s = np.sin(2 * np.pi * carrierFreq * (1.0 + 0.25 * voltage))
        # Update the clock
        clk = np.matmul(np.array( [ [c, -s], [s,c] ] ), clk )
    
        vout = np.append(vout, voltage)
        cout = np.append(cout, clk[0])
        rout = np.append(rout, np.cos(pref+2*np.pi*fref*i))
        dout0 = np.append(dout0, lpmixed[0])

           
    return vout, cout, rout, dout0

"""
BPSK Costas Loop
Demodulate a signal using costas Loop and binary phase Shift keying scheme,
cosine( 2pi * sample number * carrier freq) 
Inputs:
    txModulated:   Array of modulated data to be demodulated
    carrierFreq:   Normalised Carrier Frequency
    bitPeriod:     Number of samples to be used for each bit representation
    nBits:         Number of bits expected to Rx
    b1             FIR Filter coefficients to be used 
    
Outputs:
    vout:         Voltage oscilator waveform
    cout:         Clock waveform
    rout:         waveform 
    dout0:        Data waveform
    
"""
def CostasLoopBPSK(txModulated, carrierFreq, bitPeriod, preludeSize, nBits, b1):

    clk = ([1.0,0.0])
    fref = carrierFreq * (1. +0.02 * ( np.random.rand() - 0.5))
    pref = 2 * np.pi * np.random.rand()
    voltage = 0.0
    vout = np.array(voltage)
    cout = clk[0]
    rout = np.cos(pref)
    dout0 = np.empty(0)

    nTaps = len(b1)
    mixed = np.zeros((2, nTaps))
    lpmixed = np.empty(2) 
    
    # Append zeroes to the end of the Rx signal
    txModulated = np.append(txModulated,np.zeros(nTaps//2))

    # For all bits in the Rx bit string including additional equal to amount of taps to flush the filter
    for i in range(0,bitPeriod*(preludeSize+nBits)+nTaps//2): 
        
        # Multiplies symbol value with the cosine clock to demodulate
        mixed[0,:] = np.append(mixed[0,1:], clk[0]  * txModulated[i] ) 
        mixed[1,:] = np.append(mixed[1,1:], -clk[1] * txModulated[i] ) 
        
        # Low Pass Filtering Discrete Convolution Filtering with mixed signal
        lpmixed = [np.sum(b1*mixed[j,:]) for j in range (2)]
        # Multiply the filter outputs at a mixer to obtain voltage
        voltage = lpmixed[0] * lpmixed[1]
        
        # Try to find appropraite value for alpha to obtain correct frequency
        c = np.cos(2 * np.pi * carrierFreq * (1.0 + 0.25 * voltage))
        s = np.sin(2 * np.pi * carrierFreq * (1.0 + 0.25 * voltage))
        # Update the clock
        clk = np.matmul(np.array( [ [c, -s], [s,c] ] ), clk )
    
        vout = np.append(vout, voltage)
        cout = np.append(cout, clk[0])
        rout = np.append(rout, np.cos(pref+2*np.pi*fref*i))
        dout0 = np.append(dout0, lpmixed[0])

           
    return vout, cout, rout, dout0

  
if __name__ == "__main__":

    # Define student number
    idNum = 2536572 # 0b = 00 10 01 10 10 11 01 00 01 11 11 00
    binTestVector = [0,0,1,0,0,1,1,0,1,0,1,1,0,1,0,0,0,1,1,1,1,1,0,0]
    # Define number of bits
    nBits = 24
    # Obtain binary representation for student number
    idNumBin = BinArray(idNum,nBits)
    txBin = idNumBin
    
    preludeNBits = 16
    # Add random binary data to ensure time for clock to lock before data bits
    prelude = np.array(np.random.randint(2, size=preludeNBits), dtype="bool")
    txBin = np.append(prelude,txBin)
    
    carrierFreq = 1/32
    nBits = 24 # Add differential encoding bit 
    bitPeriod = 128

    # FIR Filter Design
    nTaps = 128
    cuttOffFrequency = 0.005
    b1 = signal.firwin(nTaps, cuttOffFrequency)
    w1, h1 = signal.freqz(b1)

    # Create matched filter by reversing FIR response
    b1 = np.flip(b1)
    
    print("Unmodulated TX Data: ")
    print(txBin)
    
    # Differnetial Encoding
    #difEncoded = DifferentialEncoder(txBin)

    # Modulate Signal Using BPSK scheme
    txBPSK = ModulationBPSK(txBin, bitPeriod, carrierFreq)

    #difEncoded = DifferentialEncoder(txBin)

    # Rx and demodulate signal using costas Loops    
    vout, cout, rout, dout0 = CostasLoop(txBin, carrierFreq, bitPeriod, nBits, b1)
    # vout, cout, rout, dout0 = CostasLoopBPSK(txBPSK, carrierFreq, bitPeriod, nBits, b1)

    
    # Run Heaviside function to detect bits in the waveform
    rxBin = np.uint8([np.heaviside(dout0[(2*i+1)*bitPeriod//2+nTaps//2],0) for i in range(prelude.size+nBits)])
    

    # Differential Decoding
    #rxBin = DifferentialDecoder(rxBin)

    
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
