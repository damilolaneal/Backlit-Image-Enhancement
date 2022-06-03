#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 23:35:59 2021

INCOMPLETE! (Look at the date XD)
Pads the image "Im" to retain its dimensions when filtered using "f".
The padding method is "mirror".

@author: ruwwad
"""

def mirrorPadIm(Im, f):
    # Pads the image to retain its dimensions when filtered using "f".
    import numpy as np
    fr = f.shape[0]  #Number of rows in the filter
    fc = f.shape[1]  #Number of columns in the filter
    x = int(np.floor(fr/2))  #Offset in the x-axis
    y = int(np.floor(fc/2))  #Offset in the y-axis
    
    ImCent = np.hstack((np.flip(Im, axis=1), Im, np.flip(Im, axis=1)))
    ImPad = np.vstack( (np.flip(ImCent, axis=0)), ImCent, (np.flip(ImCent, axis=0)) )
    
    
    # Padding the image depends on the dimensions of the filter, or rather, whether
    # they are even or not. So you could have:
        # fr: odd,   fc: odd
        # fr: odd,   fc: even
        # fr: even,   fc: odd
        # fr: even,   fc: even
    # Each of these condition requires its own equation for finding the padded
    # image. Such conditions can be accounted for using if statements. However,
    # running if statement slows the code down, and accounting for all conditions
    # does not seem to be necessary since filters almost always have odd dimensions.
    # The solution to this is to use "exception handling". This allows the code to
    # assume the filter is odd and run its associated equation, and only check the
    # conditions if an error is raised. Thus, we keep the speed while accounting
    # for all different conditions.
    try:
        Im_pad = np.zeros([Im.shape[0]+fr-1, Im.shape[1]+fc-1])
        Im_pad[x:Im_pad.shape[0]-x,y:Im_pad.shape[1]-y] = Im  # Im_pad: Guided Image Padded
    except:
        #The first if statement seems unnecessary as it duplicates the "try"
        if fr/2 != int(fr/2) and fc/2 != int(fc/2):  #Checks if the filter has odd dimensions
            Im_pad = np.zeros([Im.shape[0]+fr-1, Im.shape[1]+fc-1])
        elif fr/2 != int(fr/2) and fc/2 == int(fc/2):  #Checks if fr is odd while fc is even
            Im_pad = np.zeros([Im.shape[0]+fr-1, Im.shape[1]+fc])
        elif fr/2 == int(fr/2) and fc/2 != int(fc/2):  #Checks if fr is even while fc is odd
            Im_pad = np.zeros([Im.shape[0]+fr, Im.shape[1]+fc-1])
        else:  #Checks if the filter has even dimensions
            Im_pad = np.zeros([Im.shape[0]+fr, Im.shape[1]+fc])
        Im_pad[x:Im_pad.shape[0]-x,y:Im_pad.shape[1]-y] = Im  # Im_pad: Guided Image Padded
    return Im_pad
    