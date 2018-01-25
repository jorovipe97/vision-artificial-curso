# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:55:01 2018

@author: Jose Romualdo Villalobos Perez
"""

def clamp(val, minVal, maxVal):
    out = val
    if (val > maxVal):
        out = max
    elif (val < minVal):
        out = 0
    
    return out