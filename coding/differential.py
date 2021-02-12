# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:51:05 2021

@author: Kamil
"""

import numpy as np 

"""
Compute boolean exclusive or logical operation on two boolean variables
Inputs:
    boolean1: First boolean variable
    boolean2: Second boolean variable
    
Outputs:
    Boolean result of exclusive or logical operation  

"""
def LogicalXOR(boolean1, boolean2):
    return bool(boolean1) ^ bool(boolean2)


"""
Compute boolean exclusive or logical operation on two boolean variables
Inputs:
    binString: binary input string to be encoded
    
Outputs:
    differnetially encoded binary string

"""
def DifferentialEncoder(binString):
    # Compute number of bits
    stringLen = len(binString)
    codedString = np.zeros(1)

    # Set initial state of register to be 0 
    previousValue = 0
    
    for i in range(stringLen): 
        # Compute xor of current and previous bit 
        xor = LogicalXOR(binString[i], previousValue)
        # Append Result
        codedString = np.append(codedString, xor)
        # Put Current output through delay line of 1 step
        previousValue = xor
        
    
    if( stringLen + 1 != len(codedString)  ):
        print("Differentially encoded sring has incorrect Length: " + str(len(codedString)))
    
    return codedString
     

"""
Compute boolean exclusive or logical operation on two boolean variables
Inputs:
    binString: differentially encoded binary string to be decoded 
    
Outputs:
    differnetially decoded binary string 

"""
def DifferentialDecoder(binString):
    # Compute number of bits
    stringLen = len(binString)
    decodedString = np.empty(0) 
    
    for i in range(1,stringLen):
        # Compute xor of current and previous bit 
        xor = LogicalXOR(binString[i], binString[i-1])
        # Append Result
        decodedString = np.append(decodedString, xor)
    
    if( (stringLen - 1 ) != len(decodedString) ):
        print("Differentially decoded sring has incorrect Length: " + str(len(decodedString)))
    
    return decodedString
