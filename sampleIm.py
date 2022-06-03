#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: ruwwad
@edited: damilola
'''

#This function is capable of both downsampling and upsampling.
#It is done by finding a linear map that changes the basis of the indices
#from a rectangular basis to the basis of M.
#After that, we simply remove non integer values.
#Then, negative indices are avoided by shifting then by the minimum value of
#each axis.

# import numpy as np
# Im = np.array([[1,2,3,4],
#                 [5,6,7,8],
#                 [9,10,11,12],
#                 [13,14,15,16]])
# M = np.array([[2,0],[0,1]])
def sampleIm(Im, M):
    import numpy as np
    Im = np.array(Im) #Transforms the input image to a numpy array
    M = np.array(M) #Transforms the input image to a numpy array
    P = np.transpose(np.linalg.inv(M)) #Transformation matrix (change of basis)
    #I am not sure why P must be transposed
    sizeIm = Im.shape
    x = np.empty(Im.shape)
    y = np.empty(Im.shape)
    for i in range(sizeIm[0]):
        for j in range(sizeIm[1]):
            #Generate the values of the mapped indices
            x[i,j] = i*P[0,0] + j*P[0,1]
            y[i,j] = i*P[1,0] + j*P[1,1]
    
    #Matrix indices cannot have non-integer values.
    #To work around that, each non-integer value will be change
    fc = np.array([[],[]], dtype=int) #Coordinates of non-integer values (Float Coordinates)
    Im_c = np.copy(Im)
    for i in range(sizeIm[0]):
        for j in range(sizeIm[1]):
            if x[i,j] != round(x[i,j]) or y[i,j] != round(y[i,j]):
                fc = np.append(fc, [[i], [j]], axis=1)
    x1 = np.copy(x)
    y1 = np.copy(y)
    for i in range(fc.shape[1]):
        x1[fc[0,i],fc[1,i]] = 0
        y1[fc[0,i],fc[1,i]] = 0
        Im_c[fc[0,i],fc[1,i]] = Im[0,0]
        
        
    #We cannot have negative indices in arrays, so we will eliminate them by 
    #shifting each axis by its minimum value.
    
    x1Min = np.amin(x1)
    y1Min = np.amin(y1)
    x2 = x1 - x1Min
    y2 = y1 - y1Min
    
    #Now by using the mapped indices, the image can be properly sampled.
    g = np.zeros([round(np.amax(x2))+2, round(np.amax(y2))+2]) #Preallocation
    for i in range(sizeIm[0]):
        for j in range(sizeIm[1]):
            (m,n) = (int(x2[i,j]), int(y2[i,j]))
            g[m,n] = Im_c[i,j] #sampled imaged
    return g

# import numpy as np
# import matplotlib.pyplot as plt

# X = np.array([[i*4+j for j in range(5)] for i in range(5)])

# M1 = np.array([[4,0],[0,4]])
# M2 = np.array([[0,4],[4,0]])
# M3 = np.array([[0,1],[4,0]])
# M4 = np.array([[3,1],[1,2]])
# M = [M1, M2, M3, M4]

# L=list()
# for i in range(4):
#     L.append(np.linalg.inv(M[i]))
    
# upSamp = list()
# dnSamp = list()
# for i in range(4):
#    upSamp.append(sampleIm(X,L[i]))
#    dnSamp.append(sampleIm(X,M[i]))

# print("Downsampling:\n")
# print("The original array is:\n",X)
# print("\nDownsmapling the array by M_a:\n",dnSamp[0])
# print("\nDownsmapling the array by M_b:\n",dnSamp[1])
# print("\nDownsmapling the array by M_c:\n",dnSamp[2])
# print("\nDownsmapling the array by M_d:\n",dnSamp[3])

# print("\n\nUpsampling:\n")
# print("The original array is:\n",X)
# print("\nUpsmapling the array by L_a:\n",upSamp[0])
# print("\nUpsmapling the array by L_b:\n",upSamp[1])
# print("\nUpsmapling the array by L_c:\n",upSamp[2])
# print("\nUpsmapling the array by L_d:\n",upSamp[3])
