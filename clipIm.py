#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 02:16:47 2021

@author: ruwwad
"""

def clipIm(Im, minimum, maximum):
    #Clips the intensities of the image to certain minimum and maximum values
    #"Im" is the image
    #"minimum" is the lowest value an image should have
    #"maximum" is the highest value an image should have
    import numpy as np
    
    Im = np.array(Im)  #Converts the image into a numpy array
    if len(Im.shape) == 2:  #If the image was grayscale
        newIm= np.copy(Im)  #Preallocation
        for i in range(Im.shape[0]):
            for j in range(Im.shape[1]):
                if Im[i,j] >= maximum:
                    newIm[i,j] = maximum
                elif Im[i,j] <= minimum:
                    newIm[i,j] = minimum
    else:  #If the image was RGB
        newIm= np.copy(Im[:,:,:3])  #Limits the image to three channels to avoid errors caused by PNG
        for i in range(Im.shape[0]):
            for j in range(Im.shape[1]):
                for k in range(3):
                    if Im[i,j,k] >= maximum:
                        newIm[i,j,k] = maximum
                    elif Im[i,j,k] <= minimum:
                        newIm[i,j,k] = minimum


    # print(newIm)
    # normalizedNewIm= normIm(newIm, 0, 255)
    return newIm