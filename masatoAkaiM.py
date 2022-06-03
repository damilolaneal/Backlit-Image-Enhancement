#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 23:13:47 2021

#Implements the method found in the paper: "A SINGLE BACKLIT IMAGE ENHANCEMENT
METHOD FOR IMPROVEMENT OF VISIBILITY OF DARK PART" [1].

@author: ruwwad
"""

#Reference:
    # [1] M. Akai, Y. Ueda, T. Koga and N. Suetake, "A Single Backlit Image
    #     Enhancement Method For Improvement Of Visibility Of Dark Part," 2021
    #     IEEE International Conference on Image Processing (ICIP), 2021,
    #     pp. 1659-1663, doi: 10.1109/ICIP42928.2021.9506526.
    
def masatoAkaiM(Im):
    import numpy as np
    # import matplotlib.pyplot as plt
    from PIL import Image
    # Isn't there a cleaner way to call all functions in the same project?
    from normIm import normIm
    from otsuM import otsuM
    from histEq import histEq
    from gammaCorr import gammaCorr
    from thresholdIm import thresholdIm
    from guidedFilter import guidedFilter
    
    Im_Org = np.array(Image.open(Im), dtype=float)
    # Im_Org = np.array(Im, dtype=float)
    Im_Org = Im_Org[:,:,0:3]  #Limit the image to 3 channels to avoid edge cases (when the image has a transparency channel)
    
    if len(Im_Org.shape) == 2:
        Im = np.copy(Im_Org)
    else:
        Im = (Im_Org[:,:,0]+Im_Org[:,:,1]+Im_Org[:,:,2])/3
        # Note that the results could warp if the array type was not float,
        # resulting in a heavily distorted image
    
    (alpha, gamma) = (0.5, 2)  #Those are the values used in the paper [1]
    
    ImGamma = gammaCorr(Im, gamma)  #Applies gamma correction to the image
    ImHistEq = histEq(Im)  #Find the histogram equalized image
    
    # Now, naive alpha-blending is used to find the enhanced image
    ImEnhanced = (1-alpha)*ImGamma + alpha*ImHistEq
    
    t = otsuM(Im)  #Otsu's method is used to seperate the pixels into two classes; bright and dark
    w = 1 - thresholdIm(Im, t)  #Otsu's method applied to the input image
    
    #r: filter size
    #e: regularization parameter preventing "a" from being too large
    (r, e) = (20, 0.001) 
    wp = guidedFilter(w, Im, r, e)  #Weight map obtained by using a guided image
    # Note: some pixels in "wp" have negative values!
    # Clipping them could be a good idea
    
    #Normalization is used below because some pixels have negative values due
    #the use of the guided filter! To verify the possibility of negative values
    #resulting from the guided filter, an example was solved by hand, and it
    #achieved the same results as the ones from the above function
    outputGray = normIm(np.multiply(wp, ImEnhanced) + np.multiply(1-wp, Im), 0, 255)
    
    # The below stacks are  used to avoid errors when computing outputRGB
    outputGray3D = np.stack([outputGray, outputGray, outputGray], axis=2)
    Im3D = np.stack([Im, Im, Im], axis=2)
    
    # The below line will break if the input image was grayscale
    # Also, The value 0.5 was added to avoid division by zero
    outputRGB = np.multiply(Im_Org, np.divide(outputGray3D+0.5, Im3D+0.5))
    outputRGB = np.uint8(normIm(outputRGB, 0, 255))
    
    # plt.figure(dpi=300)
    # plt.axis('off')
    # plt.title("Masato Akai's Method")
    # plt.imshow(outputRGB)
    
    return outputRGB