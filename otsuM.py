#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 23:01:36 2021

This function uses Otsu's method to perform automatic thresholding
The algorithm is based on the equations found on the wiki
Source: https://en.wikipedia.org/wiki/Otsu%27s_method
    
@author: ruwwad
@edited: damilola
"""

def otsuM(Im):
    # This function uses Otsu's method to perform automatic thresholding
    # The algorithm is based on the equations found on the wiki
    # Source: https://en.wikipedia.org/wiki/Otsu%27s_method
    import numpy as np
    from hist import hist
    
    Im = np.array(Im)  #Converts the image into a numpy array to avoid edge-cases
    histIm = hist(Im)  #Histogram of the image
    p = histIm/np.sum(histIm)  # PDF of the histogram
    
    # Preallocation
    # w0 is the probability of all dark intensities
    # w1 is the probability of all bright intensities
    # u0 is the mean value of dark intensities
    # u1 is the mean value of bright intensities
    # v is the intra-class variance
    # r is the intensity values in the image
    # vDict is used to find the threshold that results in the maximum
    # intra-class variance. The keys are the intra-class variance, while the
    # values are the thresholds.
    
    w0 = np.zeros(histIm.shape[0]-1); w1 = np.zeros(histIm.shape[0]-1)
    u0 = np.zeros(histIm.shape[0]-1); u1 = np.zeros(histIm.shape[0]-1)
    v = np.zeros(histIm.shape[0]-1); r = np.array([i for i in range(histIm.shape[0])])
    vDict = {}
    for i in range(histIm.shape[0]-1):
        w0[i] = np.sum(p[:i+1])
        if w0[i] != 0:
            u0[i] = np.sum(r[:i+1] * p[:i+1]) / w0[i]
        else:
            u0[i] = 0
        
        w1[i] = np.sum(p[i+1:])
        if w1[i] != 0:
            u1[i] = np.sum(r[i+1:] * p[i+1:]) / w1[i]
        else:
            u1[i] = 0
        
        v[i]  = w0[i]*w1[i]*np.square(u0[i]-u1[i])
        vDict[v[i]] = np.append(vDict.get(v[i], np.array([], dtype=int)), np.array(i+1))
        # The append function is used to avoid edge-cases.
        # If two thresholds resulted in the same intra class-variance,
        # the first threshold would be overwritten. This can be avoided by
        # storing the threshold values as arrays, and then append them
        # whenever a threshold results in the same intra-class variance.
        # Hence, multiple thresholds will can now be stored.
        # Highly unlikely that this will ever happen though.
        
        
    # The if statement below helps to alert the user of multiple thresholds
    # holding the same intra-class variance.
    if vDict[np.amax(v)].shape[0] == 1:
        return vDict[np.amax(v)][0]
    else:
        print("WARNING: There are two or more thresholds with the same intra-class variance!")
        print("         The returned value is a numpy array. Use indexing to choose")
        print("         the preferred threshold.")
        return vDict[np.amax(v)]

#Example
# import numpy as np
# from hist import hist
# Im = [[0,0,1,1,1,1,1,2,2,2],
#       [2,3,3,3,3,4,4,4,4,5]]
# # histIm = np.array([2,5,4,4,4,1])
# Im = np.array([[0,1,1,2,2],
#                [1,1,0,0,2],
#                [3,3,5,5,4],
#                [2,1,6,6,4]])
# histIm = hist(Im)
# p = histIm/np.sum(histIm)

# # Preallocation
# w0 = np.zeros(histIm.shape[0]-1); w1 = np.zeros(histIm.shape[0]-1)
# u0 = np.zeros(histIm.shape[0]-1); u1 = np.zeros(histIm.shape[0]-1)
# v = np.zeros(histIm.shape[0]-1); r = np.array([i for i in range(histIm.shape[0])])
# vDict = {}
# for i in range(histIm.shape[0]-1):
#     w0[i] = np.sum(p[:i+1])
#     if w0[i] != 0:
#         u0[i] = np.sum(r[:i+1] * p[:i+1]) / w0[i]
#     else:
#         u0[i] = 0
    
#     w1[i] = np.sum(p[i+1:])
#     if w1[i] != 0:
#         u1[i] = np.sum(r[i+1:] * p[i+1:]) / w1[i]
#     else:
#         u1[i] = 0
    
#     v[i]  = w0[i]*w1[i]*np.square(u0[i]-u1[i])
#     vDict[v[i]] = np.append(vDict.get(v[i], np.array([], dtype=int)), np.array(i+1))


# #Check the validity of the code
# print('\nCheck that w0 + w1 = 1 for all thresholds')
# ut = np.sum(r*p)
# for i in range(histIm.shape[0]-1):
#     print(w0[i]+w1[i])

# print('\nCheck that w0*u0 + w1*u1 - ut = 0 for all thresholds')
# for i in range(histIm.shape[0]-1):
#     print(w0[i]*u0[i]+w1[i]*u1[i]-ut)