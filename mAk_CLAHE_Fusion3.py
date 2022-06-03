#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 00:04:12 2021

Follows the method found in [1]. However, we have made some modifications to it

1- The paper [1] uses global histogram equalization to enhance the contrast of
   the image. Since this causes artifacts and overenhancements, we used
   CLAHE [2] instead.

2- It introduces another image that is raised to the power gamma. This is used
   to extract details in the bright regions. This should be "mostly" offset
   by the weight map used by [1]. However, it does have its uses in some cases
   
3- The naive blending in [1] is replaced with image fusion from [3], which
   uses gaussain and laplacian pyramids to fuse the images.

NOTE: Using modification (2) and (3) actually yields worse results, but
      fortunately, CLAHE improves the results of [1] in terms of PIQE [4].
      Though, modification (2) does subjectively improve the results of fusion

@author: ruwwad
@edited: damilola
"""


# References:
# [1] M. Akai, Y. Ueda, T. Koga and N. Suetake, "A Single Backlit Image
#     Enhancement Method For Improvement Of Visibility Of Dark Part," 2021
#     IEEE International Conference on Image Processing (ICIP), 2021,
#     pp. 1659-1663, doi: 10.1109/ICIP42928.2021.9506526.

# [2] K. Zuiderveld, “Contrast limited adaptive histogram equalization,”
#     in Graphics gems IV, pp. 474–485, Cambridge, Academic Press, 1994.

# [3] C. Li, S. Tang, J. Yan and T. Zhou, "Low-Light Image Enhancement via
#     Pair of Complementary Gamma Functions by Fusion," in IEEE Access,
#     vol. 8, pp. 169887-169896, 2020, doi: 10.1109/ACCESS.2020.3023485.

# [4] Venkatanath N, Praneeth D, Maruthi Chandrasekhar Bh, Sumohana S.
#     Channappayya, warup S.Medasani.Blind image quality evaluation using
#     perception based features.2015 Twenty FirstNational Conference on
#     Communications.DOI: 10.1109/NCC.2015.7084843.

def mAk_CLAHE_Fusion3(Im):
    import numpy as np
    import cv2 as cv
    # import matplotlib.pyplot as plt
    from PIL import Image
    # Isn't there a cleaner way to call all functions in the same project?
    from colorSpace import rgb2hsiIm, hsi2rgbIm
    from normIm import normIm
    from otsuM import otsuM
    from hist import hist
    from gammaCorr import gammaCorr
    from thresholdIm import thresholdIm
    from guidedFilter import guidedFilter
    from fusion3 import fusion3

    Im_Org = np.array(Image.open(Im), dtype=float)
    # Im_Org = np.array(Im, dtype=float)
    Im_Org = Im_Org[:, :,
             0:3]  # Limit the image to 3 channels to avoid edge cases (when the image has a transparency channel)

    if len(Im_Org.shape) == 2:
        Im = np.copy(Im_Org)
    else:
        HSI = rgb2hsiIm(Im_Org)  # Converts the RGB image into the HSI model
        # n: Number of bits required to represent x
        n = int(np.ceil(np.log2(np.amax(np.array(Im_Org)) + 1)))
        L = 2 ** n  # Number of intensity levels available in the image

        # Transforms the range of the intensities from [0, 1] to [0, L-1]
        Im = (L - 1) * HSI[:, :, 2]

    gamma = 2  # This value is from [1]
    h = hist(Im)
    N = np.sum(h)  # Number of pixels in the image
    n = np.sum(h[:50])  # Number of pixels whose value are less than 50

    ImGamma = gammaCorr(Im, gamma)  # Applies gamma correction to the image
    gammaH = 1 / ((N - n) / N)  # The method to find gamma
    ImExp = gammaCorr(Im, 1 / gammaH)
    c = 2.0  # Should be later tweaked to improve quality
    clahe = cv.createCLAHE(clipLimit=c, tileGridSize=(8, 8))  # GridSize should be later tweaked too
    ImCLAHE = np.array(clahe.apply(np.uint8(Im)), dtype=float)

    # Now, image fusion is applied to blend the images
    l = 4  # Number of levels in the pyramid. l=4 is used in [2]
    ImEnhanced = fusion3(ImGamma, ImCLAHE, ImExp, l)

    t = otsuM(Im)  # Otsu's method is used to seperate the pixels into two classes; bright and dark
    w = 1 - thresholdIm(Im, t)  # Otsu's method applied to the input image

    # r: filter size
    # e: regularization parameter preventing "a" from being too large
    (r, e) = (20, 0.001)
    wp = guidedFilter(w, Im, r, e)  # Weight map obtained by using a guided image
    # Note: some pixels in "wp" have negative values!

    # Normalization is used below because some pixels have negative values due
    # the use of the guided filter! To verify the possibility of negative values
    # resulting from the guided filter, an example was solved by hand, and it
    # achieved the same results as the ones from the above function
    outputGray = normIm(np.multiply(wp, ImEnhanced) + np.multiply(1 - wp, Im), 0, 1)
    HSI[:, :, 2] = outputGray
    outputRGB = np.uint8(hsi2rgbIm(HSI, 8))

    # plt.figure(dpi=300)
    # plt.axis('off')
    # plt.title("y={} CLAHE(c={}), w/ Fusion_Exp".format(np.round(gamma, 2), c))
    # plt.imshow(outputRGB)
    return outputRGB
