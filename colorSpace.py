#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:44:42 2021

@author: ruwwad
"""

def rgb2hsi(r, g, b, n):
    # Convert a single element from RGB to HSI
    import numpy as np
    import math
    #r: intensity of the red channel
    #g: intensity of the green channel
    #b: intensity of the blue channel
    #n: number of bits required to represent each pixel in the image
    mx = 2**n - 1  #Maximum possible intensity value in the image
    (r,g,b) = (r/mx,g/mx,b/mx)  #Normalizes the RGB values so that the maximum intensity is equal to 1
    I = ((r+g+b)/3)  #Intensity
    S = 1 - (I and 1/I)*np.amin([r, g, b])  #Saturation
    thetaN = ((r-g)+(r-b))/2  #Numerator of theta
    thetaD = np.sqrt((r-g)**2+(r-b)*(g-b))  #Denominator of theta
    # theta = math.acos(thetaN / thetaD)  #This would break if thetaD == 0
    theta = math.acos(thetaD and thetaN / thetaD)  #Theta (used to calculate the hue)
    # An explanation to the above line is found in the link below (it is interesting):
    # https://stackoverflow.com/a/68118106
    
    if b > g:
        H = 2*np.pi - theta
    else:
        H = theta
    
    return (H, S, I)


def rgb2hsiIm(I):
    #converts the image from RGB to the HSI color model
    import numpy as np
    
    Im = np.array(I[:,:,:3])  #Converts the image into a numpy array
    iv= Im.shape[0]  #Number of rows "Im" has
    ih= Im.shape[1]  #Number of columns "Im" has
    n = int(np.ceil(np.log2(np.amax(np.array(Im))+1)))  #Number of bits required to represent I
    
    hsi = np.zeros(Im.shape)  #Preallocation
    for i in range(iv):
        for j in range(ih):
            (hsi[i,j,0], hsi[i,j,1], hsi[i,j,2]) = rgb2hsi(Im[i,j,0], Im[i,j,1], Im[i,j,2], n)
    return hsi

def hsi2rgb(h, s, i, n):
    # Converts a single element from HSI to RGB
    
    import numpy as np
    mx = 2**n -1  #Maximum possible intensity value in the RGB image
    
    # The factors below will be used to determine the values of the RGB channels
    H = h / (np.pi/3)
    z = 1 - abs((H%2) - 1)
    # z = 1 - abs((H*(180/np.pi) % 2) - 1)
    c = (3*i*s) / (1+z)
    x = c*z
    
    if H < 1:
        (r1, g1, b1) = (c, x, 0)
    elif H < 2:
        (r1, g1, b1) = (x, c, 0)
    elif H < 3:
        (r1, g1, b1) = (0, c, x)
    elif H < 4:
        (r1, g1, b1) = (0, x, c)
    elif H < 5:
        (r1, g1, b1) = (x, 0, c)
    elif H < 6:
        (r1, g1, b1) = (c, 0, x)
    
    #Notice that there's a pattern [x, c, c, x, 0, 0] in each column
    #and that each column is shifted by 2 elements from the previous column.
    #I am not sure how useful this observation is, but it is cool nevertheless :)
    
    m = i * (1-s)
    (r, g, b) = ((r1+m)*mx, (g1+m)*mx, (b1+m)*mx)
    return (r, g, b)
    
    
    # The method follows this "paper?" https://www.cse.unr.edu/~looney/cs674/mgx8/unit8.pdf
    # x = (1/3) * (1-s)
    # y = (1/3) * (1 + s * (np.cos(h) / np.cos((1/3)*pi-h)))
    # z = 1 - (x+y)
    # if h < (1/3)*(2*pi):
    #     (b, r, g) = (x, y, z)
    # elif h < (2/3)*(2*pi):
    #     (r, g, b) = (x, y, z)
    # elif h < (3/3)*(2*pi):
    #     (g, b, r) = (x, y, z)
    # else:
    #     print("Somehow, the hue is greater than 2*pi!")
    #     print("This is impossible, so go fix it!")
    # return (r, g, b)

def hsi2rgbIm(I, n):
    #converts the image from HSI to the RGB color model
    import numpy as np
    from normIm import normIm
    
    Im = np.array(I[:,:,:3])  #Converts the image into a numpy array
    iv= Im.shape[0]  #Number of rows "Im" has
    ih= Im.shape[1]  #Number of columns "Im" has
    
    rgb = np.zeros(Im.shape)  #Preallocation
    for i in range(iv):
        for j in range(ih):
            (rgb[i,j,0], rgb[i,j,1], rgb[i,j,2]) = hsi2rgb(Im[i,j,0], Im[i,j,1], Im[i,j,2], n)
    return normIm(rgb, 0, 2**n-1)


# (r,g,b)=(120,85,180)
# (h,s,i) = rgb2hsi(r, g, b, 8)
# (r1, g1, b1) = hsi2rgb(h,s,i,8)
# import numpy as np
# # loss = np.amax(np.array([r-r1, g-g1, b-b1]))
# # print(round(loss, 4))

# from PIL import Image
# I = np.array(Image.open('Images/r1RGB.png'), dtype=float)
# I = I[:,:,:3]
# conversion = hsi2rgbIm(rgb2hsiIm(I), 8)
# loss = I - conversion
# # print(round(loss, 4))