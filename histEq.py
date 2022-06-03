#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 22:17:54 2021

@author: ruwwad
"""

#Finds the equalized histogram of greyscale images
def histEq(Im):
    import numpy as np
    from hist import hist
    
    histIm = hist(Im) / Im.size
    normHist = np.zeros(histIm.shape)
    normHist[0] = np.copy(histIm[0])
    for i in range(1, len(histIm)):
        v = histIm[i]
        normHist[i] += np.sum(histIm[0:i+1])
        # print("i= {}\nv= {}\n".format(i,v))
    
      #Number of bits required to represent x
    normHist = np.round(normHist * (len(histIm)-1))
    output = np.zeros(Im.shape)
    for i in range(Im.shape[0]):
        for j in range(Im.shape[1]):
            output[i,j] = normHist[int(Im[i,j])]
    return output

# Example
# import numpy as np
# from hist import hist

# Im = np.array([[0,1,1,2,2],
#                 [1,1,0,0,2],
#                 [3,3,5,5,4],
#                 [2,1,6,6,4]])
# histIm = hist(Im) / Im.size
# normHist = np.zeros(histIm.shape)
# normHist[0] = np.copy(histIm[0])
# for i in range(1, len(histIm)):
#     v = histIm[i]
#     normHist[i] += np.sum(histIm[0:i+1])
#     # print("i= {}\nv= {}\n".format(i,v))

#   #Number of bits required to represent x
# normHist = np.round(normHist * (len(histIm)-1))
# output = np.zeros(Im.shape)
# for i in range(Im.shape[0]):
#     for j in range(Im.shape[1]):
#         output[i,j] = normHist[int(Im[i,j])]