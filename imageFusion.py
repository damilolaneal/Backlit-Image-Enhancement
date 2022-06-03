#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 22:21:10 2021

@author: ruwwad
"""

#References:
    # [1] M. Akai, Y. Ueda, T. Koga and N. Suetake, "A Single Backlit Image
    # Enhancement Method For Improvement Of Visibility Of Dark Part," 2021
    # IEEE International Conference on Image Processing (ICIP), 2021,
    # pp. 1659-1663, doi: 10.1109/ICIP42928.2021.9506526.
    
    # [2] C. Li, S. Tang, J. Yan and T. Zhou, "Low-Light Image Enhancement via
    #     Pair of Complementary Gamma Functions by Fusion," in IEEE Access,
    #     vol. 8, pp. 169887-169896, 2020, doi: 10.1109/ACCESS.2020.3023485.

import numpy as np
from filterImGray import filterImGray as filterIm #I should probably write a faster function
from filterImRGB import filterImRGB
from meanPadImRGB import meanPadImRGB
from meanPadIm import meanPadIm
from zeroPadIm import zeroPadIm
from sampleIm import sampleIm
from normIm import normIm

def exposednessWM(Im, u, std):
    # Im: Input images (yes, plural to make things tidy)
    # u: Mean
    # std: Standard deviation
    # Follows Equation (20) & (21) from reference [2]
    
    n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
    L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).
    w = 0*Im  #Preallocation
    try:
        for k in range(Im.shape[2]):
            w[:,:,k] = np.exp(-(( (Im[:,:,k]/(L-1)) - u)**2) / (2*(std**2)))
        for i in range(Im.shape[0]):
            for j in range(Im.shape[1]):
                w[i,j,:] = w[i,j,:]/np.sum(w[i,j,:])
    except:
        w = np.exp(-((Im/(L-1)-u)**2)/(2*(std)**2))
    return w

# Im_Org = np.array(Image.open('Images/r1RGB.png'), dtype=float)
# w = 0*Im_Org[:,:,:2]
# print(w.shape)
# Im = np.copy(Im_Org[:,:,:2])
# # Im = np.arange(1024).reshape((2,128,4))
# std = 0.25  #Used by reference [2]
# u = 0.5  #Used by reference [2]
# n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
# L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).

# for i in range(Im.shape[2]):
#     w[:,:,i] = np.exp(-((Im[:,:,i]/(L-1)-u)**2)/(2*(std)**2))

def upSample(Im):
    # Im: Input images (yes, plural to make things tidy)
    
    # This function upsamples the image by L=2 using bilinear interpolation
    # I realize that the code makes no sense, but I don't wanna waste time to
    # to write yet another function optimized for upsampling. What I will do
    # instead is to smooth the image using the following kernels:
        
    # fr = [[1],
    #       [1],
    #       [1]]
    
    # fc = [[1], [1], [1]]
    
    # f = [[1,1,1],
    #      [1,1,1],
    #      [1,1,1]]
    
    # The kernel fr will find interpolate the values along the m-axis
    # The kernel fc will find interpolate the values along the n-axis
    # The kernel f will find interpolate the values that have 4 neighbors
    # Then some manipulations will be used to combine all the above values
    # I know... my laziness can lead to "weird" solution at times :)
    # But my God this is so freaking SLOW!!!
    # If I had the time I would definitely optimize it, but not now.
    # Actually, the biggest problem here is that the filterIm function is
    # very slow. I wrote the same function on python and MATLAB, and MATLAB
    # is waay faster.
    
    L = np.array([[1/2,0], [0,1/2]])  #Upsampling matrix
    
    try:
        Im_Upsampled = np.zeros([2*Im.shape[0], 2*Im.shape[1], Im.shape[2]])
        for k in range(Im.shape[2]):
            print(k)
            ImUP = sampleIm(Im[:,:,k], L)  #Upsampled image WITHOUT interpolation
            ones = sampleIm(np.ones(Im[:,:,k].shape), L)  #This will be used to do some tricks
            deltaM = np.flip(ones, axis=1) / 2  #Weights along the m-axis
            deltaN = np.flip(ones, axis=0) / 2  #Weights along the n-axis
            delta4 = np.flip(ones) / 4  #Weights for values with 4 neighbors
            
            fc = np.array([[1,1,1]])
            fr = np.transpose(fc)
            f = np.ones((3,3))
            
            M = filterIm(zeroPadIm(ImUP,fc), fc)  #Interpolated values along the m-axis
            print(k)
            N = filterIm(zeroPadIm(ImUP,fr), fr)  #Interpolated values along the m-axis
            print(k)
            C = filterIm(zeroPadIm(ImUP,f), f)  #Interpolated values for values with
                                                #4 neighbors                            
            print(k)
            bilnearInterpolation = ImUP + deltaM*M + deltaN*N + delta4*C
            # The above is completely fine, but the values are halfed for the last
            # column and row since they only have 1 neighbor. Plus, the very last 
            # element very low value. I'll fix this by replicatin the of the previous
            # row and column.
            
            # ones = np.ones(ones.shape)
            fix = 2*np.ones(ones.shape)
            fix[:ones.shape[0]-1, :ones.shape[1]-1] = np.ones([ones.shape[0]-1, ones.shape[1]-1])
            fix[-1,-1] = fix[-1,-1]*2  #Fixes the last element
            # print(fix)
            Im_Upsampled[:,:,k] = bilnearInterpolation*fix
    except:
        print("0")
        ImUP = sampleIm(Im, L)  #Upsampled image WITHOUT interpolation
        ones = sampleIm(np.ones(Im.shape), L)  #This will be used to do some tricks
        deltaM = np.flip(ones, axis=1) / 2  #Weights along the m-axis
        deltaN = np.flip(ones, axis=0) / 2  #Weights along the n-axis
        delta4 = np.flip(ones) / 4  #Weights for values with 4 neighbors
        
        fc = np.array([[1,1,1]])
        fr = np.transpose(fc)
        f = np.ones((3,3))
        
        M = filterIm(zeroPadIm(ImUP,fc), fc)  #Interpolated values along the m-axis
        print("0")
        N = filterIm(zeroPadIm(ImUP,fr), fr)  #Interpolated values along the m-axis
        C = filterIm(zeroPadIm(ImUP,f), f)  #Interpolated values for values with
                                            #4 neighbors
        print("0")
        bilnearInterpolation = ImUP + deltaM*M + deltaN*N + delta4*C
        # The above is completely fine, but the values are halfed for the last
        # column and row since they only have 1 neighbor. Plus, the very last 
        # element very low value. I'll fix this by replicatin the of the previous
        # row and column.
        
        # ones = np.ones(ones.shape)
        fix = 2*np.ones(ones.shape)
        fix[:ones.shape[0]-1, :ones.shape[1]-1] = np.ones([ones.shape[0]-1, ones.shape[1]-1])
        fix[-1,-1] = fix[-1,-1]*2  #Fixes the last element
        # print(fix)
        Im_Upsampled = bilnearInterpolation*fix
        
    return Im_Upsampled

#Constructing gaussian pyramids

def gaussianPyramid(Im, l):
    # Im: Input images (yes, plural to make things tidy)
    # l: no.f level in the pyramid
    # Follows Equation (22) from reference [2]
    
    # I have my doubts about the validity of the method I have followed here.
    # I have skipped the part regarding upsampling the gaussian to obtain the
    # laplacian. Hopefully it will not impact the results too much.
    
    # f = np.ones((5,5))  #Smoothing filter (might be replaced later)
    f = np.array([[1,  4,  7,  4, 1],  # 5x5 Gaussian kernel
                  [4, 16, 26, 16, 4],
                  [7, 26, 41, 26, 7],
                  [4, 16, 26, 16, 4],
                  [1,  4,  7,  4, 1]])
    f = f / np.sum(f)  #Normalizes the filter
    
    try:
        x, y, z = Im.shape[0], Im.shape[1], Im.shape[2]
        # The padding below is done to make sure that downsampling halves the
        # image dimensions in each pyramid level
        I = np.zeros([int(np.ceil(x/2**l)*2**l), int(np.ceil(y/2**l)*2**l), z])
        I[:x,:y,:z] = np.copy(Im)
        
        g = [I]  #Gaussian pyrmaid
        blur = []  #Preallocation
        L = []  #Preallocation
        
        ds = lambda I : I[0:I.shape[0]:2, 0:I.shape[1]:2, :]#Downsample by M=2
        for i in range(l):  #Construct each level of the pyramid
            print(g[i].shape)
            blur.append(filterImRGB(meanPadImRGB(g[i], f), f))  #Used to construct L
            g.append(ds(blur[i]))  #Gaussian pyramid
            L.append(g[i] - blur[i])  #Laplacian pyramid
        L.append(g[l])
    except:
        x, y = Im.shape[0], Im.shape[1]
        # The padding below is done to make sure that downsampling halves the
        # image dimensions in each pyramid level
        I = np.zeros([int(np.ceil(x/2**l)*2**l), int(np.ceil(y/2**l)*2**l)])
        I[:x,:y] = Im
        
        g = [I]  #Gaussian pyrmaid
        blur = []  #Preallocation
        L = []  #Preallocation
        
        ds = lambda I : I[0:I.shape[0]:2, 0:I.shape[1]:2]#Downsample by M=2
        
        for i in range(l):  #Construct each level of the pyramid
            print(g[i].shape)
            blur.append(filterIm(meanPadIm(g[i], f), f))  #Used to construct L
            g.append(ds(blur[i]))  #Gaussian pyramid
            L.append(g[i] - blur[i])  #Laplacian pyramid
        L.append(g[l])
    return (g, L)

def imageFusion(Im, l):
    # Im: Input images (yes, plural to make things tidy)
    # l: no.f level in the pyramid
    # Follows Equations (20 - 22) from reference [2]
    
    n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent x
    L = 2**n  #Number of intensity levels available in the image (in other words, it is our bandwidth).
    Im = Im/(L-1)  #Normalizes the image to have a maximum value of 1
    u, std = 0.5, 0.25  #The values are taken from reference [2]
    w = exposednessWM(Im, u, std)
    gauss, dummy = gaussianPyramid(w, l)
    dummy, lap = gaussianPyramid(Im, l)
    v = []
    l += 1
    for i in range(l):
        h = gauss[i]*lap[i]
        dummy = np.zeros([h.shape[0], h.shape[1]])
        for k in range(Im.shape[2]):
            dummy += h[:,:,k]
        v.append(dummy)
    
    output = v[-1]
    for i in range(l-2, -1, -1):
        print(output.shape)
        output = upSample(output) + v[i]
    return output[:Im.shape[0], :Im.shape[1]]

def fusion(lpA, lpB, gpW0, gpW1):
    v = []
    l = len(lpA)
    for i in range(l-1, -1, -1):
        h = gpW0[l-i-1]*lpA[i] + gpW1[l-i-1]*lpB[i]
        v.append(np.copy(h))
    
    output = v[-1]
    for i in range(l-2, -1, -1):
        print(output.shape)
        output = upSample(output) + v[i]
    return output[:449, :599]

# #Testing
# import matplotlib.pyplot as plt
# Im_Org = np.array(Image.open('Images/r1RGB.png'), dtype=float)
# I = Im_Org[:,:,0]
# gauss, lap = gaussianPyramid(I, 4)

# for i in range(4):
#     plt.figure(dpi=300)
#     plt.axis('off')
# plt.imshow(gauss[i], 'gray')
# plt.title('Level = {}'.format(i))