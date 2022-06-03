#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 20:37:17 2021

@author: ruwwad
"""

# This function implement the image fusion found in reference [2].

#References:
    # [1] M. Akai, Y. Ueda, T. Koga and N. Suetake, "A Single Backlit Image
    # Enhancement Method For Improvement Of Visibility Of Dark Part," 2021
    # IEEE International Conference on Image Processing (ICIP), 2021,
    # pp. 1659-1663, doi: 10.1109/ICIP42928.2021.9506526.
    
    # [2] C. Li, S. Tang, J. Yan and T. Zhou, "Low-Light Image Enhancement via
    #     Pair of Complementary Gamma Functions by Fusion," in IEEE Access,
    #     vol. 8, pp. 169887-169896, 2020, doi: 10.1109/ACCESS.2020.3023485.

import cv2 as cv
import numpy as np,sys

A = cv.imread('PCGF_Gamma_R1.tif')
B = cv.imread('PCGF_Sharp_R1.tif')
w0 = cv.imread('ExposednessWM_Gamma.tif')
w1 = cv.imread('ExposednessWM_Sharp.tif')

# generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in range(4):
    G = cv.pyrDown(G)
    gpA.append(G)
    
# generate Gaussian pyramid for B
G = B.copy()
gpB = [G]
for i in range(4):
    G = cv.pyrDown(G)
    gpB.append(G)
    
# generate Laplacian Pyramid for A
lpA = [gpA[3]]
for i in range(3,0,-1):
    GE = cv.pyrUp(gpA[i])
    L = cv.subtract(gpA[i-1],GE)
    lpA.append(L)
    
# generate Laplacian Pyramid for B
lpB = [gpB[3]]
for i in range(3,0,-1):
    GE = cv.pyrUp(gpB[i])
    L = cv.subtract(gpB[i-1],GE)
    lpB.append(L)

# =============================================================================

G = w0.copy()
gpW0 = [G]
for i in range(4):
    G = cv.pyrDown(G)
    gpW0.append(G)
    
# generate Gaussian pyramid for B
G = w1.copy()
gpW1 = [G]
for i in range(4):
    G = cv.pyrDown(G)
    gpW1.append(G)
    
# # Now add left and right halves of images in each level
# LS = []
# for la,lb in zip(lpA,lpB):
#     rows,cols,dpt = la.shape
#     ls = np.hstack((la[:,0:cols//2], lb[:,cols//2:]))
#     LS.append(ls)
# # now reconstruct
# ls_ = LS[0]
# for i in range(1,4):
#     ls_ = cv.pyrUp(ls_)
#     ls_ = cv.add(ls_, LS[i])
# # image with direct connecting each half
# real = np.hstack((A[:,:cols//2],B[:,cols//2:]))