#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 00:37:39 2021

Find the variance of the image (returns a signle value)

@author: ruwwad
"""

def varIm(Im):
    #Find the variance of the image (returns a signle value)
    import numpy as np
    
    Im = np.array(Im)  #Converts the image into a numpy array
    avg = np.sum(Im) / Im.size  #Find the average of the image
    var = np.sum((Im - avg)**2) / Im.size  #Finds the variance
    
    return var

#Run the commands below to see how the code the runs
# import numpy as np
# (m,n) = (3, 3)  #Using odd dimensions will produce integers for most of this process
# Im = np.arange(m*n).reshape([m,n])  #An example of an image
# print("Assume Im to be the image.\nIm =\n{}".format(Im))

# avg = np.sum(Im) / Im.size
# print("\nThe average value of the image is {}".format(avg))

# print("\nSubtracting each element of the image by the average results in:\n{}".format(Im-avg))

# print("\nSquaring each element of the previous matrix results in:\n{}".format((Im - avg)**2))

# print("\nThe sum of all elements is {}".format(np.sum((Im - avg)**2)))

# var = np.sum((Im - avg)**2) / Im.size
# strFin = "\nFinally, dividing the sum by the number of elements in the image gives us the variance of the image, which is equal to {}".format(var)
# print(strFin)
