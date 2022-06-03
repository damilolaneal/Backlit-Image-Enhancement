#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 02:50:28 2021

I have written this function to make it much quicker to show high quality
figures. Plus, it does somethings that I prefer. For example, cmap='gray' is 
automatically applied to grayscale images. Another example is when I use
cmap ='gray', this automatically normalizes the image which I find to be
annoying, so this function gets rid of that. Also, it removes the useless axis
shown in the image, etc.

NOTE: I did not test running inside subplots (which is the reason for the
                                              "newFigure" parameter)
@author: ruwwad
"""

def imshow(Im, title, newFigure):
    import numpy as np
    import matplotlib.pyplot as plt
    from normIm import normIm
    Im = np.array(Im, dtype=float)  #To make sure the image is of type float
    n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
    L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).
    minimum = np.amin(Im)
    
    if newFigure == 1:
        if len(Im.shape) == 2:
            if L == 256 and (minimum >= 0):
                plt.figure(dpi=300)
                plt.axis('off')
                plt.title(title)
                plt.imshow(np.uint8(Im), 'gray', vmin=0, vmax=255)
            elif L==1 and (minimum >= 0):
                plt.figure(dpi=300)
                plt.axis('off')
                plt.title(title)
                plt.imshow(np.uint8(Im*255), 'gray', vmin=0, vmax=255)
            else:
                print("The image does NOT have a standard range... \nNormalizing...")
                plt.figure(dpi=300)
                plt.axis('off')
                plt.title(title)
                plt.imshow(normIm(Im, 0, 255), 'gray', vmin=0, vmax=255)
        elif len(Im.shape) == 3:
            if L == 256 and (minimum >= 0):
                plt.figure(dpi=300)
                plt.axis('off')
                plt.title(title)
                plt.imshow(np.uint8(Im), vmin=0, vmax=255)
            elif L==1 and (minimum >= 0):
                plt.figure(dpi=300)
                plt.axis('off')
                plt.title(title)
                plt.imshow(np.uint8(Im*255), vmin=0, vmax=255)
            else:
                print("The image does NOT have a standard range... \nNormalizing...")
                plt.figure(dpi=300)
                plt.axis('off')
                plt.title(title)
                plt.imshow(normIm(Im, 0, 255), vmin=0, vmax=255)
        else:
            print("Something isn't right with the image, so fix it!")
    else:
        if len(Im.shape) == 2:
            if L == 256 and (minimum >= 0):
                plt.axis('off')
                plt.title(title)
                plt.imshow(np.uint8(Im), 'gray', vmin=0, vmax=255)
            elif L==1 and (minimum >= 0):
                plt.axis('off')
                plt.title(title)
                plt.imshow(np.uint8(Im*255), 'gray', vmin=0, vmax=255)
            else:
                plt.axis('off')
                plt.title(title)
                plt.imshow(normIm(Im, 0, 255), 'gray', vmin=0, vmax=255)
                print("Something isn't right with the image, so fix it!")
        if len(Im.shape) == 3:
            if L == 256 and (minimum >= 0):
                plt.axis('off')
                plt.title(title)
                plt.imshow(np.uint8(Im), vmin=0, vmax=255)
            elif L==1 and (minimum >= 0):
                plt.axis('off')
                plt.title(title)
                plt.imshow(np.uint8(Im*255), vmin=0, vmax=255)
            else:
                print("The image does NOT have a standard range... \nNormalizing...")
                plt.axis('off')
                plt.title(title)
                plt.imshow(normIm(Im, 0, 1), vmin=0, vmax=255)
        else:
            print("Something isn't right with the image, so fix it!")