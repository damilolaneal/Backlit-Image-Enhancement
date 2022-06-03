#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 23:04:04 2021

@author: openCV, edited by ruwwad
"""

# References:
    # [1] M. Akai, Y. Ueda, T. Koga and N. Suetake, "A Single Backlit Image
    # Enhancement Method For Improvement Of Visibility Of Dark Part," 2021
    # IEEE International Conference on Image Processing (ICIP), 2021,
    # pp. 1659-1663, doi: 10.1109/ICIP42928.2021.9506526.
    
    # [2] C. Li, S. Tang, J. Yan and T. Zhou, "Low-Light Image Enhancement via
    #     Pair of Complementary Gamma Functions by Fusion," in IEEE Access,
    #     vol. 8, pp. 169887-169896, 2020, doi: 10.1109/ACCESS.2020.3023485.


import cv2 as cv
import numpy as np,sys
import matplotlib.pyplot as plt
from PIL import Image
from histEq import histEq
from gammaCorr import gammaCorr
from imageFusion import exposednessWM
from PCGF_gamma import PCGF_gamma
from PCGF_Sharp import PCGF_Sharp

l = 4
Im_Org = np.array(Image.open('Images/r1RGB.png'), dtype=float)
#Funny story, I've wasted about about two hours troubleshooting why the results
#were completely wrong, and it turned out the image was of type "uint8" ):
#The lesson to learn here is that you should assume that EVERYTHING COULD GO
#WRONG, EVEN THE INPUT IMAGE ITSELF!!!
Im = (Im_Org[:,:,0]+Im_Org[:,:,1]+Im_Org[:,:,2])/3  #Note that the results could warp if the array type was not float, resulting in a heavily distorted image
ImGamma = PCGF_gamma(Im, 2.2)
g = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=float)  #Smmothing kernel
ImSharp = PCGF_Sharp(Im, g, 1)

# The padding below is done to make sure that downsampling halves the
# image dimensions in each pyramid level
x, y = Im.shape[0], Im.shape[1]
A = np.zeros([int(np.ceil(x/2**l)*2**l), int(np.ceil(y/2**l)*2**l)])
# x, y, z = Im.shape[0], Im.shape[1], Im.shape[2]
# A = np.zeros([int(np.ceil(x/2**l)*2**l), int(np.ceil(y/2**l)*2**l), z])
B = np.copy(A)
dummy = np.zeros([int(np.ceil(x/2**l)*2**l), int(np.ceil(y/2**l)*2**l), 2])
        
A[:x,:y] = np.copy(ImGamma)
B[:x,:y] = np.copy(ImSharp)

w = np.zeros((A.shape[0], A.shape[1], 2))
dummy[:,:,0] = np.copy(A)
dummy[:,:,1] = np.copy(B)
w = exposednessWM(dummy, 0.5, 0.25)
w0 = np.copy(w[:,:,0])
w1 = np.copy(w[:,:,1])

# generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in range(l):
    G = cv.pyrDown(G)
    gpA.append(G)
    
# generate Gaussian pyramid for B
G = B.copy()
gpB = [G]
for i in range(l):
    G = cv.pyrDown(G)
    gpB.append(G)
    
# generate Laplacian Pyramid for A
lpA = [gpA[l-1]]
for i in range(l-1,0,-1):
    GE = cv.pyrUp(gpA[i])
    L = cv.subtract(gpA[i-1],GE)
    lpA.append(L)
    
# generate Laplacian Pyramid for B
lpB = [gpB[l-1]]
for i in range(l-1,0,-1):
    GE = cv.pyrUp(gpB[i])
    L = cv.subtract(gpB[i-1],GE)
    lpB.append(L)
    
G = w0.copy()
gpW0 = [G]
for i in range(l):
    G = cv.pyrDown(G)
    gpW0.append(G)
    
# generate Gaussian pyramid for B
G = w1.copy()
gpW1 = [G]
for i in range(l):
    G = cv.pyrDown(G)
    gpW1.append(G)
    
# Now add left and right halves of images in each level
LS = []
i = -1
for la,lb in zip(lpA,lpB):
    # rows,cols,dpt = la.shape
    i += 1
    rows,cols = la.shape
    ls = gpW0[(l-1)-i]*la + gpW1[(l-1)-i]*lb
    # ls = np.hstack((la[:,0:cols//2], lb[:,cols//2:]))
    LS.append(ls)
# for la,lb in zip(lpA,lpB):
#     # rows,cols,dpt = la.shape
#     rows,cols = la.shape
#     ls = np.hstack((la[:,0:cols//2], lb[:,cols//2:]))
#     LS.append(ls)

# now reconstruct
ls_ = LS[0]
for i in range(1,l):
    ls_ = cv.pyrUp(ls_)
    ls_ = cv.add(ls_, LS[i])
    
# image with direct connecting each half
real = np.hstack((A[:,:cols//2],B[:,cols//2:]))

# real = np.hstack((A[:,:cols//2],B[:,cols//2:]))

# plt.figure(dpi=300)
# plt.subplot(1,2,1)
# plt.axis('off')
# plt.imshow(ls_[:x,:y]/255, 'gray')

# plt.subplot(1,2,2)
# plt.axis('off')
# plt.imshow(real[:x,:y]/255, 'gray')

plt.figure(dpi=300)
plt.imshow(ls_[:x,:y]/255, 'gray')