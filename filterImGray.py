#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 23:01:36 2021

@author: ruwwad
"""
# from PIL import Image
# from matplotlib import pyplot as plt

def filterImGray(Im, f):
    #Applies a filter to an image
    #"Im" is the image
    #"f" is the filter
    import numpy as np
    
    Im = np.array(Im)  #Converts the image into a numpy array
    f = np.flip(np.array(f))  #Converts the filter into a numpy array.
                              #The filter is flipped to perform convolution.
                              #Otherwise, it will perform correlation instead.
    #Flipping the filter is essential to perform proper convolution.
    #Convolving an image with a 2D impluse should result in the same image.
    #This can easily be proved by setting:
        #delta=np.zeros((5,5)); delta[2,2]=1; f = np.arange(9).reshape(3,3)
        #filterImGray(delta, f)
    #The output should be "f"
    
    #f_sz = np.flip(np.append([1,1,1,1], np.array(f.shape)))  #Size of "f"
    f_sz = f.shape  # Size of "f"
    fv= f_sz[0]  #Number of rows "f" has
    fh= f_sz[1]  #Number of columns "f" has
    
    i_sz = Im.shape  #Size of "Im"
    iv= i_sz[0]  #Number of rows "Im" has
    ih= i_sz[1]  #Number of columns "Im" has
    
    if fv > iv or fh > ih:
        (Im, iv, ih, f, fv, fh) = (f, fv, fh, Im, iv, ih)  #Edge case: The user swapped the filter with the image
    
    xi= (fv-1) / 2   #Initial point in x
    xf= iv - xi - 1    #Final point in x
    yi= (fh-1) / 2   #Initial point in y
    yf= ih - yi - 1    #Final point in y
    # print(xi,xf,yi,yf)
    # newIm= np.zeros([ic, int(xf-xi+1), int(yf-yi+1)])
    newIm= np.zeros([int(xf-xi+1), int(yf-yi+1)])
    
    for i in np.arange(xi, xf+1):
        for j in np.arange(yi, yf+1):
            # np.arange() was chosen instead of range() to allow "i" to
            # use decimal values, which allows it to work with filters
            # that have even dimensions. Does not make sense, but the
            # code would still function normally this way.
            fr= [r for r in np.arange((i-xi),(i-xi+fv), dtype=int)]  #Indices of filtered rows
            fc= [c for c in np.arange((j-yi),(j-yi+fh), dtype=int)]  #Indices of filtered columns
            window= Im[fr[0]:fr[-1]+1, fc[0]:fc[-1]+1]  #This line could be rewritten for efficiency
            # As
            product= np.multiply(f[:,:],window)
            # print(fc)
            # print(window)
            # print(product)
            # print(np.sum(product))
            newIm[fr[0], fc[0]]= np.sum(np.sum(product))
    # print(newIm)
    # normalizedNewIm= normIm(newIm, 0, 255)
    return newIm
