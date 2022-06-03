#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 23:18:30 2021

@author: ruwwad
"""

# Applies gamma correction to the image
def gammaCorr(Im, gamma):
    
    import numpy as np
    n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
    mx = 2**n - 1  #Maximum "possible" intensity in the image
    #Consider using the actual maximum value in the image
    output = np.zeros(Im.shape)
    for i in range(Im.shape[0]):
        for j in range(Im.shape[1]):
            output[i,j] = mx * (Im[i,j]/mx)**(1/gamma)  #Gamma correction equation
    return output
        
# Im = np.array([[0,1,1,2,2],
#                [1,1,0,0,2],
#                [3,3,5,5,4],
#                [2,1,6,6,4]])
# gamma = 2