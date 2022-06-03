#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 23:33:28 2021

@author: ruwwad
@edited: damilola
"""

'''Sharpens the image using an unsharp mask according to reference [1]'''
# References:
    # [1] C. Li, S. Tang, J. Yan and T. Zhou, "Low-Light Image Enhancement via
    #     Pair of Complementary Gamma Functions by Fusion," in IEEE Access,
    #     vol. 8, pp. 169887-169896, 2020, doi: 10.1109/ACCESS.2020.3023485.
import numpy as np
from filterImGray import filterImGray as filterIm
from histEq import histEq
from meanPadIm import meanPadIm
from clipIm import clipIm

# def unsharpMask(Im, g, a):
#     # Sharpens the image using the unsharp mask
#     print(np.sum(g))
#     blurIm = filterIm(meanPadIm(Im, g), g) / np.sum(g)
#     return Im + a * (Im - blurIm)

def PCGF_Sharp(Im, g, alpha):
    #Sharpens the image using an unsharp mask according to reference [1]
    #Im: Grayscale input image as a numpy array
    #g: Gaussian kernel
    #alpha: Sharpening strength
    
    # Im_Pad = meanPadIm(Im, g)  #Padded image to preserve its dimensions after convolution
    blurIm = lambda I, f: filterIm(meanPadIm(I, f), f) / np.sum(f) #Blurs the image
    unsharpMask = lambda I, f, a: I + a * (I - blurIm(I, f)) #Sharpens the image
    # It's highly appreciated if the unsharpMask was clipped to have a maximum
    # value of (L-1).
    
    histV = histEq(Im)  #Applies histogram equalization to the image
    # n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
    # L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).
    # s2 = normIm(unsharpMask(histV, g, alpha), 0, L-1)
    s2 = unsharpMask(histV, g, alpha)
    output = (Im + s2)/2
    return output

# # import numpy as np
# # from histEq import histEq
# # from hist import hist
# # from filterImGray import filterImGray as filterIm
# # from meanPadIm import meanPadIm
# from filterImGray import filterImGray as filterIm
# # from normIm import normIm
# from PIL import Image

# Im_Org = np.array(Image.open('Images/r1RGB.png'), dtype=float)
# Im = Im_Org[:,:,1]
# g = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=float)
# alpha = 3

# # Im_Pad = meanPadIm(Im, g)  #Padded image to preserve its dimensions after convolution
# unsharpMask = lambda I, f, a: I + a * (I - (filterIm(meanPadIm(I, f), f)/np.sum(f)))
# # It's highly appreciated if the unsharpMask was clipped to have a maximum value of (L-1)
# print(Im.shape)
# histV = histEq(Im)
# n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
# L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).
# # s2 = normIm(unsharpMask(histV, g, alpha), 0, L-1)
# s2 = unsharpMask(histV, g, alpha)
# output = (Im + s2)/2