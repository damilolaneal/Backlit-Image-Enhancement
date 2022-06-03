#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 02:48:11 2021

Follows the method found in the paper [1], but modifies it a bit.
It replaces the histogram equalization method used in the above paper with
PCGF_Sharp.py. This should decrease the artifacts found in the image

@author: ruwwad
@edited: damilola
"""

#References:
    # [1] M. Akai, Y. Ueda, T. Koga and N. Suetake, "A Single Backlit Image
    #     Enhancement Method For Improvement Of Visibility Of Dark Part," 2021
    #     IEEE International Conference on Image Processing (ICIP), 2021,
    #     pp. 1659-1663, doi: 10.1109/ICIP42928.2021.9506526.
    
    # [2] C. Li, S. Tang, J. Yan and T. Zhou, "Low-Light Image Enhancement via
    #     Pair of Complementary Gamma Functions by Fusion," in IEEE Access,
    #     vol. 8, pp. 169887-169896, 2020, doi: 10.1109/ACCESS.2020.3023485.

def mAk_PCGF_Sharp(Im):
    import numpy as np
    # import matplotlib.pyplot as plt
    # from PIL import Image
    # Isn't there a cleaner way to call all functions in the same project?
    # from colorSpace import rgb2hsiIm, hsi2rgbIm
    from normIm import normIm
    from otsuM import otsuM
    # from histEq import histEq
    from gammaCorr import gammaCorr
    from thresholdIm import thresholdIm
    from guidedFilter import guidedFilter
    from PCGF_Sharp import PCGF_Sharp
    # from masatoAkaiM import masatoAkaiM
    
    # Im_Org = np.array(Image.open('Images/r1.png'), dtype=float)
    Im_Org = np.array(Im, dtype=float)
    # Im_Org = np.stack([Im_Org, Im_Org, Im_Org], axis=2)  #To avoid errors if the input was grayscale. Will probably change it later
    Im_Org = Im_Org[:,:,0:3]  #Limit the image to 3 channels to avoid edge cases (when the image has a transparency channel)
    
    if len(Im_Org.shape) == 2:
        Im = np.copy(Im_Org)
    else:
        Im = (Im_Org[:,:,0]+Im_Org[:,:,1]+Im_Org[:,:,2])/3  #Note that the results could warp if the array type was not float, resulting in a heavily distorted image
        # HSI = rgb2hsiIm(Im_Org)
        # n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
        # L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).
        # Im = (L-1)*HSI[:,:,2]  #Transforms the range of the intensities from [0, 1] to [0, L-1]
    
    (alpha, gamma) = (0.6, 2)
    
    ImGamma = gammaCorr(Im, gamma)  #Applies gamma correction to the image
    # ImHistEq = histEq(Im)  #Find the histogram equalized image
    g = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=float) #Gaussian kernel
    ImHistEq = PCGF_Sharp(Im, g, 1)  #Sharpens the image according to [2]
    ImEnhanced = (1-alpha)*ImGamma + alpha*ImHistEq  #Finds the enhanced image
    
    t = otsuM(Im)  #Otsu's method is used to seperate the pixels into two classes; bright and dark
    w = 1 - thresholdIm(Im, t)  #Otsu's method applied to the input image
    
    (r, e) = (1, 0.001)  #r: filter size, e: regularization parameter preventing "a" from being too large
    wp = guidedFilter(w, Im, r, e)  #Weight map obtained by using a guided image
    # Note: some pixels in "wp" have negative values!
    
    outputGray = normIm(np.multiply(wp, ImEnhanced) + np.multiply(1-wp, Im), 0, 255)  #Normalization is used because some pixels have negative values!
    
    outputGray3D = np.stack([outputGray, outputGray, outputGray], axis=2)  #To avoid errors when computing outputRGB
    Im3D = np.stack([Im, Im, Im], axis=2)  #To avoid errors when computing outputRGB
    outputRGB = np.multiply(Im_Org, np.divide(outputGray3D+0.5, Im3D+0.5))  #Would break if the input image was grayscale
    # HSI[:,:,2] = outputGray  #Shouldn't this by divided by (L-1)?
    # outputRGB = hsi2rgbIm(HSI, 8)
    
    # import matplotlib.pyplot as plt
    # plt.figure(dpi=300)
    # plt.subplot(1,2,1)
    # plt.axis('off')
    # plt.title("Original Method")
    # plt.imshow(masatoAkaiM(Im_Org))
    
    # plt.subplot(1,2,2)
    # plt.axis('off')
    # plt.title("PCGF Sharp (a=3)")
    # plt.imshow(np.uint8(outputRGB))
    
    # The value 0.5 was added to avoid division by zero
    return normIm(outputRGB, 0, 255)  # np.uint8
# plt.figure(dpi=300);plt.subplot(1,2,1);plt.axis('off');plt.title("Original Method");plt.imshow(mak);plt.subplot(1,2,2);plt.axis('off');plt.title("PCGF Sharp (a=3)");plt.imshow(np.uint8(outputRGB1))

# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
# # Isn't there a cleaner way to call all functions in the same project?
# from normIm import normIm
# from otsuM import otsuM
# from histEq import histEq
# from gammaCorr import gammaCorr
# from thresholdIm import thresholdIm
# from guidedFilter import guidedFilter
# # from zeroPadIm import zeroPadIm
# # from filterImRGB import filterImRGB as filterIm
# # from varIm import varIm
# # from varMat import varMat
# from hist import hist

# Im_Org = np.array(Image.open('Images/r1RGB.png'), dtype=float)
# Im_Org = Im_Org[:,:,:3]
# # Im_Org = Im_Org[0:2160:10,0:3840:10,0:3]  #Limit the image to 3 channels to avoid edge cases (when the image has a transparency channel)

# if len(Im_Org.shape) == 2:
#     Im = np.copy(Im_Org)
# else:
#     Im = (Im_Org[:,:,0]+Im_Org[:,:,1]+Im_Org[:,:,2])/3  #Note that the results could clip causing a severe drop in brightness

# (alpha, gamma) = (0.5, 2)

# ImGamma = gammaCorr(Im, gamma)  #Applies gamma correction to the image
# ImHistEq = histEq(Im)  #Find the histogram equalized image
# ImEnhanced = (1-alpha)*ImGamma + alpha*ImHistEq  #Finds the enhanced image

# t = otsuM(Im)  #Otsu's method is used to seperate the pixels into two classes; bright and dark
# w = 1 - thresholdIm(Im, t)  #Otsu's method applied to the input image

# (r, e) = (1, 0.001)  #r: filter size, e: regularization parameter preventing "a" from being too large
# wp = guidedFilter(w, Im, r, e)  #Weight map obtained by using a guided image
# # Note: some pixels in "wp" have negative values!

# outputGray = normIm(np.multiply(wp, ImEnhanced) + np.multiply(1-wp, Im), 0, 255)  #Normalization is used because some pixels have negative values!

# outputGray3D = np.stack([outputGray, outputGray, outputGray], axis=2)  #To avoid errors when computing outputRGB
# Im3D = np.stack([Im, Im, Im], axis=2)  #To avoid errors when computing outputRGB
# outputRGB = np.multiply(Im_Org, np.divide(outputGray3D, Im3D))  #Would break if the input image was grayscale
# #Plotting the histogram of the image at different stages

# plt.figure(dpi=300)
# plt.axes('off')
# plt.subplot(1,1,1)
# plt.plot(hist(Im))
# plt.subplot(1,1,1)
# plt.plot(hist(ImEnhanced))
# plt.subplot(1,1,1)
# plt.plot(hist(outputGray))
# plt.subplot(1,1,1)
# plt.plot(hist(outputRGB))

# plt.subplot(1,1,1)
# plt.imshow(normIm(Im,0,1), cmap="gray")
# plt.subplot(1,1,1)
# plt.imshow(normIm(ImEnhanced,0,1), cmap="gray")
# plt.subplot(1,1,1)
# plt.imshow(normIm(outputGray,0,1), cmap="gray")
# plt.subplot(1,1,1)
# plt.figure(dpi=300)

# plt.imshow(normIm(outputRGB,0,1))
# plt.axis('off')

# plt.figure(dpi=300); plt.subplot(1,3,1); plt.axis('off'); plt.imshow(I); plt.figure(dpi=300); plt.subplot(1,3,2); plt.axis('off'); plt.imshow(np.uint8(paperOutput)); plt.figure(dpi=300); plt.subplot(1,3,3); plt.axis('off'); plt.imshow(mk)