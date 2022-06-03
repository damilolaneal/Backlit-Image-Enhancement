#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 00:04:27 2021

Applies a threshold to an image

@author: ruwwad
"""

def thresholdIm(Im, t):
    #Applies a threshold to an image
    #"Im" is the image
    #"t" is the threshold value
    import numpy as np
    
    Im = np.array(Im)  #Converts the image into a numpy array
    newIm= np.zeros(Im.shape)
    
    for i in range(Im.shape[0]):
        for j in range(Im.shape[1]):
            if Im[i,j] < t:
                newIm[i,j] = 0
            else:
                newIm[i,j] = 1
    return newIm