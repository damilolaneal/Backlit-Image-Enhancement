#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 22:07:38 2021

Normalizes the image "Im" from "L" to "H"

@author: ruwwad
"""

def normIm(Im, L, H):
    # Normalizes the image from "L" to "H"
    import numpy as np
    
    Im = np.array(Im)  #Converts the image into a numpy array
    Im1 = Im - np.amin(Im)  #Sets the minimum value to zero
    Im2 = Im1 / np.amax(Im1)  #Sets the maximum value to one
    Im3 = Im2 * (H - L)  #Sets the new dynamic range of the image
    normalizedIm = Im3 + L  #Sets the new minimum and maximum value of the image to "L" and "H" respectively
    return normalizedIm