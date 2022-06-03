#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 03:10:17 2021

This function compares the use of a variance filter to a Sobel filter

@author: ruwwad
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from varMat import varMat
from filterImGray import filterImGray as filterIm
from imshow import imshow
from clipIm import clipIm

images = []
var = []
Sobel = []
fx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
fy = -np.transpose(fx)

for i in range(1, 4+1):
    Im_Org = np.array(Image.open('Images/r{}RGB.png'.format(i)), dtype=float)
    Im = (Im_Org[:, :, 0]+Im_Org[:, :, 1]+Im_Org[:, :, 2])/3
    images.append(Im)

for i in range(4):
    var.append(varMat(images[i], np.ones((3, 3)))[0, :, :])
    Sx = filterIm(images[i], fx)
    Sy = filterIm(images[i], fy)
    Sobel.append(np.sqrt(Sx**2 + Sy**2))


sTitle = ["Sobel Filter", "Sobel Filter", "Sobel Filter**(1/2)"]
vTitle = ["Variance", "Variance**(1/2)", "Variance**(1/3.8)"]
for i in range(4):
    imshow(images[i], "Input Image", 1)
    plt.figure(dpi=600)

    plt.subplot(3, 2, 1)
    plt.axis('off')
    plt.title(sTitle[0])
    plt.imshow(Sobel[i], 'gray')

    plt.subplot(3, 2, 2)
    plt.axis('off')
    plt.title(vTitle[0])
    plt.imshow(var[i], 'gray')

    plt.subplot(3, 2, 3)
    plt.axis('off')
    plt.title(sTitle[1])
    plt.imshow(Sobel[i], 'gray')

    plt.subplot(3, 2, 4)
    plt.axis('off')
    plt.title(vTitle[1])
    plt.imshow(var[i]**(1/2), 'gray')

    plt.subplot(3, 2, 5)
    plt.axis('off')
    plt.title(sTitle[2])
    plt.imshow(Sobel[i]**(1/2), 'gray')

    plt.subplot(3, 2, 6)
    plt.axis('off')
    plt.title(vTitle[2])
    plt.imshow(var[i]**(1/3.8), 'gray')
