#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 21:27:59 2021

@author: Ruwwad & Munzir
"""
# import numpy as np
import numpy as np
# Isn't there a cleaner way to call all functions in the same project?
from zeroPadIm import zeroPadIm
from filterImGray import filterImGray as filterIm
from normIm import normIm
from varMat import varMat
#from varIm import varIm  #Probably will not be needed

def guidedFilter(w, Im, r, e):
    # w: input image  (called "p" in the reference)
    # Im: guidance image
    # r: filter size
    # e: regularization parameter preventing "a" from being too large
    f_r = 2*r+1  #Size of the filter
    f = np.ones([f_r, f_r])  #Averaging filter
    f = f / np.sum(f)  #Normalizes the filter. Could be combined with the above line
    
    Im = np.array(Im)  # Im: guidance image
    Im_norm = normIm(Im, 0, 1)  #normalizes the image from 0 to 1
    #Im_norm = Im/255  #divides the image by 255 (normalization)
    Im_pad = zeroPadIm(Im_norm, f)  #Pads the image to maintain its dimension after convolving with the filter
    u = filterIm(Im_pad, f)  #u: Average of Im (Type: array)
    v = varMat(Im_pad, f)  #v: Variance of Im (Type: array)
    
    w_pad = zeroPadIm(w, f)  #Pads the image to maintain its dimension after convolving with the filter
    w_avg = filterIm(w_pad, f)  #w: w average (called p bar
    
    g = np.multiply(Im_pad, w_pad)
    g_p = filterIm(g, f)
    
    u_w_avg = np.multiply(u, w_avg)
    
    numerator = g_p - u_w_avg  #numerator of a_k
    
    a_k = np.divide(numerator, v+e)
    
    b_k = w_avg - np.multiply(a_k, u)  #There is possibly a typo in the paper "A SINGLE BACKLIT IMAGE ENHANCEMENT METHOD FOR IMPROVEMENT OF VISIBILITY OF DARK PART"
    # in computes b_k using unnomralized Im, which conflicts with the reference paper,
    # so we have decided to stick to the method proposed by the reference paper.
    
    a_k_avg = filterIm(zeroPadIm(a_k[0,:,:], f), f)
    b_k_avg = filterIm(zeroPadIm(b_k[0,:,:], f), f)
    
    w_tilde = np.multiply(a_k_avg, Im_norm) + b_k_avg
    return w_tilde

# (n,m) = (4,4)
# (r, e) = (1, 0.001)  #r: filter size, e: regularization parameter preventing "a" from being too large

# f_r = 2*r+1  #Size of the filter
# f = np.ones([f_r, f_r])  #Averaging filter
# f = f / np.sum(f)

# A = np.ones([2,4])
# B = np.zeros([2,4])
# Im = np.array([[0.1, 0.2, 0.2, 0.1],
#               [0.5, 0.4, 0.6, 0.55],
#               [0.8, 0.85, 0.9, 0.9],
#               [1  ,    1,   1,   1]])

# Im = np.array([[0,0,1,1],
#                [2,2,0,0],
#                [0,3,3,0]])

# # Im = np.arange(n*m).reshape((n,m))  # Im: guidance image
# Im_norm = normIm(Im, 0, 3)  #normalizes the image from 0 to 1
# #Im_norm = Im/255  #divides the image by 255 (normalization)
# Im_pad = zeroPadIm(Im_norm, f)
# u = filterIm(Im_pad, f)  #Im: Im average
# v = varMat(Im_pad, f)


# # w = np.random.randint(0, 1+1, Im.shape)  # p: input image (replace
# A = np.ones([2,4])
# B = np.zeros([2,4])
# D = np.array([[0.1, 0.2, 0.2, 0.1],
#               [0.5, 0.4, 0.6, 0.55],
#               [0.8, 0.85, 0.9, 0.9],
#               [1  ,    1,   1,   1]])
# w = np.append(B, A, axis=0)

# w = np.array([[1,1,1,1],
#               [0,0,0,0],
#               [0,0,0,0]])
# # w_tilde = np.zeros([1])
# w_pad = zeroPadIm(w, f)
# w_avg = filterIm(w_pad, f)  #w: w average (In the reference, it is "p" bar)

# g = np.multiply(Im_pad, w_pad)
# g_p = filterIm(g, f)

# u_w_avg = np.multiply(u, w_avg)

# numerator = g_p - u_w_avg  #numerator of a_ij

# a_k = np.divide(numerator, v+e)

# b_k = w_avg - np.multiply(a_k, u)  #There is possibly a typo in the paper "A SINGLE BACKLIT IMAGE ENHANCEMENT METHOD FOR IMPROVEMENT OF VISIBILITY OF DARK PART"
# # in computes b_k using unnomralized Im, which conflicts with the reference paper,
# # so we have decided to stick to the method proposed by the reference paper.

# a_k_avg = filterIm(zeroPadIm(a_k[0,:,:], f), f)
# b_k_avg = filterIm(zeroPadIm(b_k[0,:,:], f), f)

# w_tilde = np.multiply(a_k_avg, Im_norm) + b_k_avg



# =============================================================================
# # from PIL import Image
# # import matplotlib.pyplot as plt
# 
# # plt.plot([i for i in range(256)], hist(E))
# 
# # im = Image.open('Images/r1.png')
# # im.show
# # E = np.uint8(im)[:,:,0]
# # image = Image.fromarray(E)
# =============================================================================


# xi = int(np.floor(f_r/2))
# Im_pad = np.zeros([Im.shape[0]+2*r, Im.shape[1]+2*r])
# Im_pad[xi:-xi,xi:-xi]=Im  # Im_pad: Guided Image Padded
# w_pad = np.zeros([w.shape[0]+2*r, w.shape[1]+2*r])  #zero padding
# w_pad[xi:-xi,xi:-xi]=w
# w_avg = filterIm(w_pad, f)  #w: w average  p: p bar
# The lines are probably repeated
# w_pad = np.zeros([w.shape[0]+2*r, w.shape[1]+2*r])  #zero padding
# w_pad[xi:-xi,xi:-xi]=w
# w_avg = filterIm(w_pad, f)  #w: w average  p: p bar