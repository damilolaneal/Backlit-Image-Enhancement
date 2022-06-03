#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 00:16:24 2021

@author: ruwwad
"""

def varMat(Im, f):
    #Applies a variance filter to an image
    #Im: the input grayscale image
    #f: Filter. The code only uses the dimensions of "f" to determine
    #   the size of the variance filter (yes, the wording is messy... I know)
    #output: Array (Squaring it should result in a similar image to the output
    #        of a Sobel filter
    import numpy as np
    from varIm import varIm  #Could this line be "cleaner" than this?
    
    Im = np.array(Im)  #Converts the image into a numpy array
    # The below if statements will be explained shortly
    if len(Im.shape) == 1:
        Im = np.array([[Im]])
    elif len(Im.shape) == 2:
        Im = np.array([Im])
    elif len(Im.shape) != 3:
        return print("Error: The image has more than three dimensions!")
    
    f = np.array(f)  #Converts the filter into a numpy array
    f = np.ones(f.shape)
    if len(f.shape) == 1:
        f = np.array([[f]])
    elif len(f.shape) == 2:
        f = np.array([f])
    elif len(f.shape) != 3:
        return print("Error: The filter has more than three dimensions!")
    
    # The purpose of the above if statements is to increase the dimensions of
    # the image (or filter) to allow the code to function with both greyscale
    # and RGB images.
    # Without doing this, some edge cases could cause issues.
    # For example, assume you have the following vector:
    # V = [1, 2, 3]
    # If we were to access the second element, we would write:
    # >> V[1]
    # But, assume we entered the following instead:
    # >> V[0,1]
    # Theoretically, this is correct. The element resides in the first row 
    # and the second column. But, python would return an error since the
    # vector only has one dimension, yet we entered two dimensions to its
    # indices.
    # This can be avoided by artificially adding dimensions to the image,
    # which is why we did so.regularization parameter preventing ak from being too large
    
    #f_sz = np.flip(np.append([1,1,1,1], np.array(f.shape)))  #Size of "f"
    f_sz = f.shape  # Size of "f"
    fv= f_sz[1]  #Number of rows "f" has
    fh= f_sz[2]  #Number of columns "f" has
    fc= f_sz[0]  #Number of channels "f" has
    
    i_sz = Im.shape  #Size of "Im"
    iv= i_sz[1]  #Number of rows "Im" has
    ih= i_sz[2]  #Number of columns "Im" has
    ic= i_sz[0]  #Number of channels "Im" has
    
    if fv > iv or fh > ih:  # or fc > ic:
        (Im, f) = (f, Im)  #Edge case: The user swapped the filter with the image
        #Note: the last condition does not seem to be required
        f_sz = f.shape  # Size of "f"
        fv= f_sz[1]  #Number of rows "f" has
        fh= f_sz[2]  #Number of columns "f" has
        fc= f_sz[0]  #Number of channels "f" has
        
        i_sz = Im.shape  #Size of "Im"
        iv= i_sz[1]  #Number of rows "Im" has
        ih= i_sz[2]  #Number of columns "Im" has
        ic= i_sz[0]  #Number of channels "Im" has
    
    xi= (fv-1) / 2   #Initial point in x
    xf= iv - xi - 1    #Final point in x
    yi= (fh-1) / 2   #Initial point in y
    yf= ih - yi - 1    #Final point in y
    # print(xi,xf,yi,yf)
    newIm= np.zeros([ic, int(xf-xi+1), int(yf-yi+1)])
    
    for k in range(ic):
            for i in np.arange(xi, xf+1):
                for j in np.arange(yi, yf+1):
                    # np.arange() was chosen instead of range() to allow "i" to
                    # use decimal values, which allows it to work with filters
                    # that have even dimensions. Does not make sense, but the
                    # code would still function normally this way.
                    fr= [r for r in np.arange((i-xi),(i-xi+fv), dtype=int)]  #Indices of filtered rows
                    fc= [c for c in np.arange((j-yi),(j-yi+fh), dtype=int)]  #Indices of filtered columns
                    window= Im[k, fr[0]:fr[-1]+1, fc[0]:fc[-1]+1]  #This line could be rewritten for efficiency
                    # print(fc)
                    # print(window)
                    newIm[k, fr[0], fc[0]]= varIm(window)
    # print(newIm)
    # normalizedNewIm= normIm(newIm, 0, 255)
    return newIm


# import numpy as np
    
# Im = np.arange(16).reshape((4,4))
# f = np.ones([3,3])/9
# # The below if statements will be explained shortly
# if len(Im.shape) == 1:
#     Im = np.array([[Im]])
# elif len(Im.shape) == 2:
#     Im = np.array([Im])
# elif len(Im.shape) != 3:
#     print("Error: The image has more than three dimensions!")

# f = np.array(f)
# if len(f.shape) == 1:
#     f = np.array([[f]])
# elif len(f.shape) == 2:
#     f = np.array([f])
# elif len(f.shape) != 3:
#     print("Error: The filter has more than three dimensions!")

# # The purpose of the above if statements is to increase the dimensions of
# # the image (or filter) to allow the code to function with both greyscale
# # and RGB images.
# # Without doing this, some edge cases could cause issues.
# # For example, assume you have the following vector:
# # V = [1, 2, 3]
# # If we were to access the second element, we would write:
# # >> V[1]
# # But, assume we entered the following instead:
# # >> V[0,1]
# # Theoretically, this is correct. The element resides in the first row 
# # and the second column. But, python would return an error since the
# # vector only has one dimension, yet we entered two dimensions to its
# # indices.
# # This can be avoided by artificially adding dimensions to the image,
# # which is why we did so.

# #f_sz = np.flip(np.append([1,1,1,1], np.array(f.shape)))  #Size of "f"
# f_sz = f.shape  # Size of "f"
# fv= f_sz[1]  #Number of rows "f" has
# fh= f_sz[2]  #Number of columns "f" has
# fc= f_sz[0]  #Number of channels "f" has

# i_sz = Im.shape  #Size of "Im"
# iv= i_sz[1]  #Number of rows "Im" has
# ih= i_sz[2]  #Number of columns "Im" has
# ic= i_sz[0]  #Number of channels "Im" has

# if fv > iv or fh > ih:  # or fc > ic:
#         (Im, f) = (f, Im)  #Edge case: The user swapped the filter with the image
#         #Note: the last condition does not seem to be required
    
# xi= (fv-1) / 2   #Initial point in x
# xf= iv - xi - 1    #Final point in x
# yi= (fh-1) / 2   #Initial point in y
# yf= ih - yi - 1    #Final point in y

# newIm= np.zeros([ic, int(xf-xi+1), int(yf-yi+1)])

# for k in range(ic):
#         for i in np.arange(xi, xf+1):
#             for j in np.arange(yi, yf+1):
#                 fr= [r for r in np.arange((i-xi),(i-xi+fv), dtype=int)]  #Indices of filtered rows
#                 fc= [c for c in np.arange((j-yi),(j-yi+fh), dtype=int)]  #Indices of filtered columns
#                 window= Im[k, fr[0]:fr[-1]+1, fc[0]:fc[-1]+1]  #This line could be rewritten for efficiency
#                 # As
#                 product= np.multiply(f[k,:,:],window)
#                 # print(fc)
#                 # print(window)
#                 # print(np.sum(product))
#                 newIm[k, fr[0], fc[0]]= np.sum(np.sum(product))
# # print(newIm)
# # normalizedNewIm= normIm(newIm, 0, 255)
