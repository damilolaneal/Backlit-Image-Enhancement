#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 15:38:09 2021

@author: ruwwad
"""

# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
# from colorSpace import rgb2hsiIm, hsi2rgbIm

def preserveColor(function, args):
    # function: callable function
    # arg: Arguments used in the callable function, assume first entry to be
    #      the image. Type: List
    
    import numpy as np
    from colorSpace import rgb2hsiIm, hsi2rgbIm
    Im = np.copy(args[0][:,:,:3])  #Limits the image to 3 channels
    
    HSI = rgb2hsiIm(Im)  #Converts the image from RGB to HSI color model
    n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
    L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).
    I = (L-1)*HSI[:,:,2]  #Intensity channel and its range is [0, L-1]
    
    if len(args) == 1:
        HSI[:,:,2] = (1/(L-1)) * function(I)
    elif len(args) == 2:
        HSI[:,:,2] = (1/(L-1)) * function(I, args[1])
    elif len(args) == 3:
        HSI[:,:,2] = (1/(L-1)) * function(I, args[1], args[2])
    elif len(args) == 4:
        HSI[:,:,2] = (1/(L-1)) * function(I, args[1], args[2], args[3])
    elif len(args) == 5:
        HSI[:,:,2] = (1/(L-1)) * function(I, args[1], args[2], args[3], args[4])
    elif len(args) == 6:
        HSI[:,:,2] = (1/(L-1)) * function(I, args[1], args[2], args[3], args[4], args[5])
    elif len(args) == 7:
        HSI[:,:,2] = (1/(L-1)) * function(I, args[1], args[2], args[3], args[4], args[5], args[6])
    
    outputRGB = hsi2rgbIm(HSI, 8)
    return outputRGB

# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
# Im_Org = np.array(Image.open('Images/r1RGB.png'), dtype=float)
# Im = np.copy(Im_Org[:,:,:3])  #Limits the image to 3 channels


# HSI = rgb2hsiIm(Im)  #Converts the image from RGB to HSI color model
# n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
# L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).
# I = (L-1)*HSI[:,:,2]  #Transforms the range of the intensities from [0, 1] to [0, L-1]

# #Import callable function below:
# from PCGF_Sharp import PCGF_Sharp
# HSI[:,:,2] = (1-(L-1)) * PCGF
# outputRGB = hsi2rgbIm(HSI, 8)