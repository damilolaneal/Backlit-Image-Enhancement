#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 01:06:04 2021

Pads RGB image with mean value to retain its dimensions when filtered using "f"

@author: ruwwad
"""

def meanPadImRGB(Im, f):
    # Pads the image with mean value to retain its dimensions when filtered using "f".
    import numpy as np
    fr = f.shape[0]  #Number of rows in the filter
    fc = f.shape[1]  #Number of columns in the filter
    x = int(np.floor(fr/2))  #Offset in the x-axis
    y = int(np.floor(fc/2))  #Offset in the y-axis
    u = np.sum(Im)/np.size(Im)  #Mean value of the image
    
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
        Im_pad = u*np.ones([Im.shape[0]+fr-1, Im.shape[1]+fc-1, Im.shape[2]])
        Im_pad[x:Im_pad.shape[0]-x,y:Im_pad.shape[1]-y, :] = Im
    except:
        #The first if statement seems unnecessary as it duplicates the "try"
        if fr/2 != int(fr/2) and fc/2 != int(fc/2):  #Checks if the filter has odd dimensions
            Im_pad = u*np.ones([Im.shape[0]+fr-1, Im.shape[1]+fc-1, Im.shape[2]])
            print("odd")
        elif fr/2 != int(fr/2) and fc/2 == int(fc/2):  #Checks if fr is odd while fc is even
            Im_pad = u*np.ones([Im.shape[0]+fr-1, Im.shape[1]+fc, Im.shape[2]])
        elif fr/2 == int(fr/2) and fc/2 != int(fc/2):  #Checks if fr is even while fc is odd
            Im_pad = u*np.ones([Im.shape[0]+fr, Im.shape[1]+fc-1, Im.shape[2]])
        else:  #Checks if the filter has even dimensions
            Im_pad = u*np.ones([Im.shape[0]+fr, Im.shape[1]+fc, Im.shape[2]])
        
        Im_pad[x:Im_pad.shape[0]-x,y:Im_pad.shape[1]-y, :] = Im
    return Im_pad