#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 23:04:04 2021

This function implements image fusion according to reference [2]
Note that I have tried to write this function myself, but I couldn't get the
same results, so due to the lack of time, I taken much a code from OpenCV that 
on performs blending using image pyramids. Still, I had a lot of hiccups to get
it to work according to reference [2].

OpenCV: Image Pyramids:
    https://docs.opencv.org/4.x/dc/dff/tutorial_py_pyramids.html

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
import numpy as np
import matplotlib.pyplot as plt
from imageFusion import exposednessWM

def fusion(ImA, ImB, l):
    # l = 4
    # The padding below is done to make sure that downsampling halves the
    # image dimensions in each pyramid level
    x, y = ImA.shape[0], ImA.shape[1]
    A = np.zeros([int(np.ceil(x/2**l)*2**l), int(np.ceil(y/2**l)*2**l)])
    # x, y, z = Im.shape[0], Im.shape[1], Im.shape[2]
    # A = np.zeros([int(np.ceil(x/2**l)*2**l), int(np.ceil(y/2**l)*2**l), z])
    B = np.copy(A)
    dummy = np.zeros([int(np.ceil(x/2**l)*2**l), int(np.ceil(y/2**l)*2**l), 2])
            
    A[:x,:y] = np.copy(ImA)  #Padding ImA
    B[:x,:y] = np.copy(ImB)  #Padding ImB
    
    w = np.zeros((A.shape[0], A.shape[1], 2))  #Preallocation
    dummy[:,:,0] = np.copy(A)
    dummy[:,:,1] = np.copy(B)
    w = exposednessWM(dummy, 0.5, 0.25)  #Exposedness weight map
    w0 = np.copy(w[:,:,0])  #Exposedness weight map for ImA
    w1 = np.copy(w[:,:,1])  #Exposedness weight map for ImB
    
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
        
    # Now, use the weight maps to fuse the images
    LS = []
    i = -1
    for la,lb in zip(lpA,lpB):
        i += 1
        rows,cols = la.shape
        ls = gpW0[(l-1)-i]*la + gpW1[(l-1)-i]*lb
        LS.append(ls)
    
    # now reconstruct
    ls_ = LS[0]
    for i in range(1,l):
        ls_ = cv.pyrUp(ls_)
        ls_ = cv.add(ls_, LS[i])
    
    # plt.figure(dpi=300)
    # plt.axis('off')
    # plt.imshow(ls_[:x,:y]/255, 'gray')
    return ls_[:x,:y]
