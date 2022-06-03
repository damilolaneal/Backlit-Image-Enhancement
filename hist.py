#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 22:09:14 2021

@author: ruwwad
"""

def hist(Im):
    import numpy as np
    # Finds the histogram of the image
    # This function has two assumptions:
    # 1- The minimum intensity is zero
    # 2- All intensity values are integers
    # print(Im)
    Im = np.array(Im)  #Converts the image into a numpy array to avoid edge-cases
    # The if statement below allow the function to find the histogram of:
    # 1- greyscale images.
    # 2- RGB images.
    # 3- Videos of rgb images.
    if len(Im.shape) == 1:
        Im = np.array([[[Im]]])
    elif len(Im.shape) == 2:
        Im = np.array([[Im]])
    elif len(Im.shape) == 3:
        Im = np.array([Im])
    # print(Im)
    n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
    histo = np.zeros(2**n)  #Initializes the histogram
    for i in range(Im.shape[0]):
        for j in range(Im.shape[1]):
            for k in range(Im.shape[2]):
                for n in range(Im.shape[3]):
                    histo[int(Im[i,j,k,n])] += 1
    return histo


# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt

# Im = np.array(Image.open('Images/r1.png'), dtype=float)
# if len(Im.shape) == 1:
#     Im = np.array([[[Im]]])
# elif len(Im.shape) == 2:
#     Im = np.array([[Im]])
# elif len(Im.shape) == 3:
#     Im = np.array([Im])
# # print(Im)
# n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
# print("n =", n)
# histo = np.zeros(2**n)  #Initializes the histogram
# for i in range(Im.shape[0]):
#     for j in range(Im.shape[1]):
#         for k in range(Im.shape[2]):
#             for n in range(Im.shape[3]):
#                 histo[int(Im[i,j,k,n])] += 1