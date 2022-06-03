#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 22:56:04 2021

This function applies PCGF to the image according to the reference [1]

@author: ruwwad
"""

# References:
    # [1] C. Li, S. Tang, J. Yan and T. Zhou, "Low-Light Image Enhancement via
    #     Pair of Complementary Gamma Functions by Fusion," in IEEE Access,
    #     vol. 8, pp. 169887-169896, 2020, doi: 10.1109/ACCESS.2020.3023485.
    
import numpy as np
from colorSpace import rgb2hsiIm, hsi2rgbIm

def gammaCorrT(Im, gamma):
    # Applies gamma correction to the image according to the reference [1]
    n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
    mx = 2**n - 1  #Maximum "possible" intensity in the image
    #Consider using the actual maximum value in the image
    output = np.zeros(Im.shape)
    for i in range(Im.shape[0]):
        for j in range(Im.shape[1]):
            # output[i,j] = mx *(1 - (1 - Im[i,j]/mx)**(1/gamma) ) #Gamma correction equation
            output[i,j] = mx *((1 - (1 - Im[i,j]/mx)**(1/gamma))**gamma ) #Gamma correction equation
    return output

def crtCorr(Im, gamma):
    # Applies CRT gamma correction to the image according to the reference [1]
    n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
    mx = 2**n - 1  #Maximum "possible" intensity in the image
    #Consider using the actual maximum value in the image
    output = np.zeros(Im.shape)
    for i in range(Im.shape[0]):
        for j in range(Im.shape[1]):
            output[i,j] = mx *(1 - (1 - Im[i,j]/mx)**(gamma) ) #Gamma correction equation
    return output

def PCGF_gamma(Im_Org, gamma):
    # Applies PCGF to the image according to the reference [1]
    # The below statement checks if the input image is RGB
    if len(Im_Org.shape) == 2:
        RGB = False
        I = np.copy(Im_Org)
    else:
        RGB = True
        # Im = (Im_Org[:,:,0]+Im_Org[:,:,1]+Im_Org[:,:,2])/3  #Note that the results could warp if the array type was not float, resulting in a heavily distorted image.
        HSI = rgb2hsiIm(Im_Org) #Used to preserve color when computing the PCGF
        n = int(np.ceil(np.log2(np.amax(np.array(Im_Org))+1)))  #Number of bits required to represent x
        L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).
        I = (L-1)*HSI[:,:,2]  #Transforms the range of the intensities from [0, 1] to [0, L-1]
    y1 = crtCorr(I, gamma)  #Applies inverse gamma correction
    y2 = gammaCorrT(I, gamma) ##Applies gamma correction
    v1 = np.sum(y1)/np.size(y1) #Average value of y1
    v2 = np.sum(y2)/np.size(y2) #Average value of y2
    (c1, c2) = (v1/(v1+v2), v2/(v1+v2))  #Coefficients used for naive blending.
    y = c1*y1 + c2*y2 #Output intensity channel
    if RGB:
        HSI[:,:,2] = y
        output = hsi2rgbIm(HSI, 8)
    else:
        output = y
    return output

# from PIL import Image
# import matplotlib.pyplot as plt
# Im_Org = np.array(Image.open('Images/r1RGB.png'), dtype=float)[:,:,:1]
# gamma = 1/2.2
# gamma2= 2.2
# # alpha = 0.75
# s='Y:/D/Users/KiiRadov/Documents/1- University/Programming/Python/KFUPM MSc/Term 211/EE 663   Image Processing/A_Single_Backlit_Image_Enhancement_Method_For_Improvement_Of_Visibility_Of_Dark_Part/Images/r1RGB.png'
# ref = np.array(Image.open(s), dtype=float)[:,:,:3]
# refGamma = gammaCorr(ref, gamma)
# refGammaT = gammaCorrT(ref, 1/gamma)
# refCRTT = gammaCorrT(ref, gamma)
# refCRT = crtCorr(ref, gamma)
# alpha = np.sum(refGamma)/np.size(refGamma)
# beta = np.sum(refCRT)/np.size(refCRT)
# (alpha, beta) = (alpha/(alpha+beta), beta/(alpha+beta))
# delta = alpha

# Im = np.array([np.arange(256)])
# gc = gammaCorr(Im,gamma)[0,:]
# crt = crtCorr(Im,gamma)[0,:]
# gcT = gammaCorrT(Im,gamma2)[0,:]
# crtT = gammaCorrT(Im,1/gamma2)[0,:]
# PCGF = alpha*refGamma + beta*refCRT
# gcCRT = delta*gcT + (1-delta)*crtT

# plt.figure(dpi=300)
# plt.plot(Im[0,:], label='Straight Line')

# plt.plot(crt, label='CRT Gamma')
# plt.plot(gc, label='GC')
# plt.plot(alpha*gc + beta*crt, label='PCGF')
# # plt.plot(gcCRT, label='GC + CRT')

# plt.legend()

# plt.plot(127*np.ones(256), Im[0,:], 'k:')
# plt.plot(Im[0,:], 127*np.ones(256), 'k:')
# plt.xlabel("Input intensity")
# plt.ylabel("Output intensity")
# plt.title("Transformation")
# plt.grid()
# # Im = np.array([[0,1,1,2,2],
# #                [1,1,0,0,2],
# #                [3,3,5,5,4],
# #                [2,1,6,6,4]])
# # gamma = 2


# plt.figure(dpi=1200)
# plt.subplot(2,2,1)
# plt.axis('off')
# plt.title('Original Image')
# plt.imshow(ref/255)

# plt.subplot(2,2,2)
# plt.axis('off')
# plt.title('GC')
# plt.imshow(refGamma/255)

# plt.subplot(2,2,4)
# plt.axis('off')
# plt.title('CRT Gamma')
# plt.imshow(refCRT/255)

# plt.subplot(2,2,3)
# plt.axis('off')
# plt.title('PCGF')
# plt.imshow(PCGF/255)

# std = 0.25
# u = 0.5

# w = np.exp(-((Im[0,:]/255-u)**2)/(2*(std)**2))
# plt.figure(dpi=300)
# plt.plot(Im[0,:]/255, w)
# plt.xlabel("Input intensity")
# plt.ylabel("Output intensity")
# plt.title('Weight Map Transformation')