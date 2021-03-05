# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 10:52:21 2021

@author: Kamil
"""

import numpy as np 
from PIL import Image 
from matplotlib import pyplot as plt
import komm
from scipy import signal
import scipy
import math


"""
Simulating Bit Error Rate
This function demonstrates the effects of Signal-to-Noise(SNR) on bit errorr rate(BER)

Inputs:
    snrArray:      Array containing SNR to be investigated.
    txBin:         Input binary array
    Npixels        Number of  FIR Filter coefficients to be used 
    modulatioInfo  Modulation dictionary containg the details of modulation scheme to be used.
    
Outputs:
    berArray      Array containing BER for range of SNR
    errfcDataSet  Array containing theorethical BER for range of SNR

"""
def SimulateBER(snrArray, txBin, Npixels, modulatioInfo):
    nSNR = len(snrArray)
    rxDataArray = np.empty(len(txBin))
    BitErrorArray = np.empty(2)
    berArray = np.empty(0) 
    mod = 0
    
    # Create Modulation Scheme Object
    if( modulatioInfo.get("mod") == "PSK"):
        mod = komm.PSKModulation(modulatioInfo.get("order"))
        
    if( modulatioInfo.get("mod") == 'QAM'):
        mod = komm.QAModulation(modulatioInfo.get("order"))
        # Normalize energy per symbol
        baseAmplitude = 1/(np.sqrt(mod.energy_per_symbol))
        mod = komm.QAModulation(modulatioInfo.get("order"), baseAmplitude)
  
    print("Modulation to be used:")
    print(str(modulatioInfo.get("order")) + " " + str(modulatioInfo.get("mod")))
    print("Bits Per Symbol: " + str(mod.bits_per_symbol) ) 
    print("Energy Per Symbol: " + str(mod.energy_per_symbol))
    print("\n")

    # Modulate Data
    txData = mod.modulate(txBin)

    # For each transmision 
    for i in range(nSNR):
        # Calculate based on db
        awgn = komm.AWGNChannel(snr=10**(snrArray[i]/10.))
        # Simulate noise in channel
        rxData = awgn(txData)
        # Demodulate Data
        rxBin = mod.demodulate(rxData)
        # Append demodulated data as a new row
        rxDataArray = np.vstack([rxDataArray, rxBin])
    
    awgn = komm.AWGNChannel(snr=10**(snrArray[10]/10.))
    rx_data = awgn(txData)
    rx_bin = mod.demodulate(rx_data)
    
    # Plot few rx bits 
    plt.figure()
    plt.axes().set_aspect("equal")
    plt.scatter(rx_data[:10000].real,rx_data[:10000].imag,s=1,marker=".")
    plt.show()
    rx_im = np.packbits(rx_bin).reshape(tx_im.size[1],tx_im.size[0])
    
    plt.figure()
    plt.imshow(np.array(rx_im),cmap="gray",vmin=0,vmax=255)
    plt.show()
    

    # Measuring Bit Error Ratio
    # For each transmision
    for j in range(1,nSNR+1):
        # Reset number of bit errors
        BitErrorCount = 0
        
        # Compute bit errors
        # i.e For each pixel
        for i in range(Npixels*8):
            # If pixel value does not match
            if( rxDataArray[j][i] != txBin[i] ):
                # Increment error count
                BitErrorCount += 1
        # Calculate bit error rate for transmision
        ber = BitErrorCount / (Npixels*8)
        berArray = np.append(berArray,ber)
        # Append new dimension containing bit count and bit error rate
        BitErrorArray = np.vstack([BitErrorArray, [BitErrorCount,ber]])

    print("Bit Error Array:")
    print(BitErrorArray)
    print("\n")
    plt.figure()
    plt.scatter(snrArray, berArray) #plot points
    plt.plot(snrArray, berArray)    #plot lines
    plt.yscale("log")
    plt.ylabel('$BER$')
    plt.xlabel('$SNR$')
    plt.title((str(modulatioInfo.get("order")) + " " + str(modulatioInfo.get("mod"))))
    plt.grid(True)
    #plt.show()
    
    # Calculate theoretical BER 
    # Modify k parameter i.e. bits per symbol
    k = mod.bits_per_symbol

    errfcDataSet = np.empty(0)
    # For Each SNR
    for i in range(nSNR):
        # Calculate Theorethical BER
        errfc = 0.5* scipy.special.erfc(math.sqrt((10**(snrArray[i]/10))/k))           
        errfcDataSet = np.append(errfcDataSet,errfc)
    plt.plot(snrArray, errfcDataSet, color = 'r')
    plt.show()

    print("Errfc Data Set:")
    print(errfcDataSet)
    print("\n")
    return berArray, errfcDataSet

"""
Simulating Bit Error Rate
This function demonstrates the effects of Signal-to-Noise(SNR) on bit errorr rate(BER)

Inputs:
    snrArray:      Array containing SNR to be investigated.
    txBin:         Input binary array
    Npixels        Number of  FIR Filter coefficients to be used 
    modulatioInfo  Modulation dictionary containg the details of modulation scheme to be used.
    
Outputs:
    ARQ, , 
    ber, 
    rxBinDecoded

"""
def SimulateParityBits(snrArray, txBin, Npixels, modulatioInfo):
    nSNR = len(snrArray)
    rxBinDecoded = np.empty(0)
    rxIncorrect = True 
    
    mod = 0
    if( modulatioInfo.get("mod") == "PSK"):
        mod = komm.PSKModulation(modulatioInfo.get("order"))
        
    if( modulatioInfo.get("mod") == 'QAM'):
        mod = komm.QAModulation(modulatioInfo.get("order")) # add baseAmplitude
        print("Base Amplitude is: " + str(mod.energy_per_symbol))
        # Normalize Enerhy per symbol
        baseAmplitude = 1/(np.sqrt(mod.energy_per_symbol))
        print("New Base Amplitude is: " + str(baseAmplitude))
        mod = komm.QAModulation(modulatioInfo.get("order"), baseAmplitude)
        
        
    print("Modulation to be used:")
    print(str(modulatioInfo.get("order")) + " " + str(modulatioInfo.get("mod")))
    print("Bits Per Symbol: " + str(mod.bits_per_symbol) ) 
    print("Energy Per Symbol: " + str(mod.energy_per_symbol))
    print("\n")
    print("Simulating ARQ based on parity bit check!")


    print("Adding Parity Bits!")
    # Add parity bits    
    # For each pixel
    for i in range(Npixels):
        startIndex = i*8
        # If the sum of on bits is not even
        if((( np.sum(txBin[startIndex:startIndex+7]) ) % 2 ) != 0):
            # Change parity bit to 1
            txBin[(startIndex+7)] = 1 
        # The sum of on bits is even
        else:
            # Change parity bit to 0
            txBin[(startIndex+7)] = 0

    # Modulate data
    txDataParity = mod.modulate(txBin)
    print("Simulating Transmision!")
    indexFactor = int( 8 / mod.bits_per_symbol)
    berArray = np.empty(0) 
    arqArray = np.empty(0)
    
    for c in range(nSNR):
        print("Simulating SNR: " + str(snrArray[c]))
        # Set Average Gausian Noise to reflect new SNR
        awgn = komm.AWGNChannel(snr=10**(snrArray[c]/10.))
        ARQ = 0  
        # For Each Symbol
        for i in range(Npixels):
            # Compute Index of the codeword
            startIndex = i*indexFactor
            # Until the Parity bit check is not passed
            while(rxIncorrect):
                # Simulate noise in the channel during transmision only 
                rxData = awgn(txDataParity[startIndex:startIndex+indexFactor])
                # Demodulate Data
                rxBin = mod.demodulate(rxData) 
                # Check if parity = 0 
                if(( np.sum(rxBin) % 2 ) != 0):
                    # Error During Transmision
                    # Increment Request Counter
                    ARQ += 1
                else:
                    # Passed parity check, assume data is correct
                    # Append Data Bits to final binary array
                    rxBinDecoded = np.append(rxBinDecoded,rxBin)
                    # Set while loop flag to false indicating this codeword has been rx without error
                    rxIncorrect = False
                    
            #Set while loop flag to true to process next codeword
            rxIncorrect = True
        
        
        
        # Convert to real int
        rxBinDecoded = np.real(rxBinDecoded)
        rxBinDecoded = rxBinDecoded.astype(int)
        # For SNR 10 Plot graphs
        if(c == 0):
            # Plot few rx bits 
            # plt.figure()
            # plt.axes().set_aspect("equal")
            # plt.scatter(rxBinDecoded[:10000].real,rxBinDecoded[:10000].imag,s=1,marker=".")
            # plt.show()
            rx_im = np.packbits(rxBinDecoded).reshape(tx_im.size[1],tx_im.size[0])
            
            plt.figure()
            plt.imshow(np.array(rx_im),cmap="gray",vmin=0,vmax=255)
            plt.show()

        # Count Bit errors
        print("Computing BER: " + str(snrArray[c]))
        BitErrorCount = 0
        # For each bit in the rx data
        for i in range(Npixels*8):
            # If bit value does not match
            if( rxBinDecoded[i] != txBin[i] ):
                # Increment error count
                BitErrorCount += 1
            # Calculate bit error rate for the transmision
        berArray = np.append( berArray, (BitErrorCount / (Npixels*8)) ) 
        arqArray = np.append( arqArray, (ARQ/(Npixels*8)) )
        
   
    print("BER Array:")
    print(berArray)
    print("\n")
    
    print("ARQ Array:")
    print(arqArray)
    print("\n")

    plt.figure()
    plt.scatter(snrArray, berArray) #plot points
    plt.plot(snrArray, berArray)    #plot lines
    plt.yscale("log")
    plt.ylabel('$BER$')
    plt.xlabel('$SNR$')
    plt.title((str(modulatioInfo.get("order")) + " " + str(modulatioInfo.get("mod")) + " BER"))
    plt.grid(True)
    
    # Calculate theoretical BER 
    # Modify k parameter i.e. bits per symbol
    k = mod.bits_per_symbol

    errfcDataSet = np.empty(0)
    # For Each SNR
    for i in range(nSNR):
        # Calculate Theorethical BER
        errfc = 0.5* scipy.special.erfc(math.sqrt((10**(snrArray[i]/10))/k))           
        errfcDataSet = np.append(errfcDataSet,errfc)
    plt.plot(snrArray, errfcDataSet, color = 'r')
    plt.show()
    

    plt.figure()
    plt.scatter(snrArray, arqArray) #plot points
    plt.plot(snrArray, arqArray)    #plot lines
    plt.yscale("log")
    plt.ylabel('$ARQ Rate$')
    plt.xlabel('$SNR$')
    plt.title((str(modulatioInfo.get("order")) + " " + str(modulatioInfo.get("mod")) + " ARQ/nBits"))
    plt.grid(True)
    
    return berArray, arqArray, rxBinDecoded

if __name__ == "__main__":
    
    # Load an image
    tx_im = Image.open("DC4_300x200.pgm") #  DC4_600x400 # DC4_300x200
    # Calculate the number of pixel in image
    Npixels = tx_im.size[1]*tx_im.size[0]
    # Diplay image
    plt.figure()
    plt.imshow(np.array(tx_im),cmap="gray",vmin=0,vmax=255)
    plt.show()
    # Format bits into one dimensional array
    txBin = np.unpackbits(np.array(tx_im))
    
    # Set Modulation Schemes
    modulatioInfo  = { "mod": "PSK", "order": 2 }
    modulatioInfo1 = { "mod": "PSK", "order": 4 }
    modulatioInfo2 = { "mod": "QAM", "order": 4 }
    modulatioInfo3 = { "mod": "QAM", "order": 16 }
    modulatioInfo4 = { "mod": "QAM", "order": 256 }
    modulationSchemes = [modulatioInfo, modulatioInfo1, modulatioInfo2, modulatioInfo3, modulatioInfo4]
    
    # Set SNR Array
    #snr = np.linspace(20,1,num=20) 
    # for i in range(len(modulationSchemes)):
    #     SimulateBER(snr, txBin, Npixels, modulationSchemes[i])
        
    snr = np.linspace(10,5,num=6) 
    for i in range(len(modulationSchemes)):
        
        SimulateParityBits(snr, txBin, Npixels, modulationSchemes[i])
        
    


    
    