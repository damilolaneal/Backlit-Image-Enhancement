#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 01:49:30 2021

Follows the method found in paper [1], but it was modified as follows:

1- It replaces the global histogram equalization method used in [1] by
   PCGF_Sharp.py. This should decrease the artifacts found in the image.

2- Moreover, the naive blending is replaced with image fusion from [2], which
uses gaussain and laplacian pyramids to fuse the images.

@author: ruwwed
"""

#References:
    # [1] M. Akai, Y. Ueda, T. Koga and N. Suetake, "A Single Backlit Image
    #     Enhancement Method For Improvement Of Visibility Of Dark Part," 2021
    #     IEEE International Conference on Image Processing (ICIP), 2021,
    #     pp. 1659-1663, doi: 10.1109/ICIP42928.2021.9506526.
    
    # [2] C. Li, S. Tang, J. Yan and T. Zhou, "Low-Light Image Enhancement via
    #     Pair of Complementary Gamma Functions by Fusion," in IEEE Access,
    #     vol. 8, pp. 169887-169896, 2020, doi: 10.1109/ACCESS.2020.3023485.

def mAk_PCGF_Sharp_Fusion(Im):
    import numpy as np
    # import matplotlib.pyplot as plt
    # from PIL import Image
    # Isn't there a cleaner way to call all functions in the same project?
    from colorSpace import rgb2hsiIm, hsi2rgbIm
    from normIm import normIm
    from otsuM import otsuM
    from gammaCorr import gammaCorr
    from thresholdIm import thresholdIm
    from guidedFilter import guidedFilter
    from PCGF_Sharp import PCGF_Sharp
    from masatoAkaiM import masatoAkaiM
    from fusion import fusion
    
    # Im_Org = np.array(Image.open('Images/r1.png'), dtype=float)
    Im_Org = np.array(Im, dtype=float)
    Im_Org = Im_Org[:,:,0:3]  #Limit the image to 3 channels to avoid edge cases (when the image has a transparency channel)
    
    if len(Im_Org.shape) == 2:
        Im = np.copy(Im_Org)
    else:
        HSI = rgb2hsiIm(Im_Org)
        n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
        L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).
        Im = (L-1)*HSI[:,:,2]  #Transforms the range of the intensities from [0, 1] to [0, L-1]
    
    gamma = 2.2  #The value of gamma = 2.2 in [1]
    ImGamma = gammaCorr(Im, gamma)  #Applies gamma correction to the image
    g = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=float) #Gaussian kernel
    ImSharp = PCGF_Sharp(Im, g, 1)  #Sharpens the image according to [2]
    
    l = 4  #Number of levels in the pyramid. l=4 is used in [2]
    ImEnhanced = fusion(ImGamma, ImSharp, l)  #Image fusion according to [2]
    
    t = otsuM(Im)  #Otsu's method is used to seperate the pixels into two classes; bright and dark
    w = 1 - thresholdIm(Im, t)  #Otsu's method applied to the input image
    
    (r, e) = (20, 0.001)  #r: filter size, e: regularization parameter preventing "a" from being too large
    wp = guidedFilter(w, Im, r, e)  #Weight map obtained by using a guided image
    # Note: some pixels in "wp" have negative values!
    
    outputGray = normIm(np.multiply(wp, ImEnhanced) + np.multiply(1-wp, Im), 0, 1)  #Normalization is used because some pixels have negative values!
    
    #Convert the image back to RGB
    HSI[:,:,2] = outputGray
    outputRGB = hsi2rgbIm(HSI, 8)
    
    import matplotlib.pyplot as plt
    plt.figure(dpi=300)
    plt.subplot(1,2,1)
    plt.axis('off')
    plt.title("Original Method")
    plt.imshow(masatoAkaiM(Im_Org))
    
    plt.subplot(1,2,2)
    plt.axis('off')
    plt.title("PCGF_Sharp+Fusion")
    plt.imshow(outputRGB)
    
    return outputRGB