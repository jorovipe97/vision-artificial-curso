# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 07:05:44 2018

@author: Jose Romualdo Villalobos Perez
"""

import numpy as np
import cv2
import configurations as conf
import HelperFunctions as helper

img_original = cv2.imread("colorado.jpg", cv2.IMREAD_COLOR)
height, width, chanels = img_original.shape

img_original_grayscale = cv2.imread("colorado.jpg", cv2.IMREAD_GRAYSCALE);
height_bw, width_bw = img_original_grayscale.shape

img_out_3_channels = np.zeros((height, width, 3), np.uint8)
img_out_1_channel = np.zeros((height, width), np.uint8)


for i in range(0, 4):
    print(i)


########################
### Shaders programs ###
########################
def doNothing(colorVector):
    return colorVector


# Reto1: A Gray Scale algorithm
def grayScaleShader(colorVector, outChannels):
    conf.outImgChannels = outChannels;
    
    mean = np.mean(colorVector); # Calcule the mean
    if (conf.outImgChannels == conf.OUT_3_CHANNELS):        
        return np.array([mean, mean, mean]);
    elif (conf.outImgChannels == conf.OUT_1_CHANNEL):
        return mean;

# Bright and contrast for grayscale image
def brightAndContrastBW(pixelVal, brightness, contrast):
    conf.outImgChannels = conf.OUT_1_CHANNEL #save the output image in 1 channel
    
    outVal = (pixelVal + brightness)*contrast
    
    if (outVal > 255):
        outVal = 255
    elif (outVal < 0):
        outVal = 0
    
    # Clamp the out val between 0 and 255    
    return outVal

def brightAndContrast(colorVec, brightness, contrast):
    conf.outImgChannels = conf.OUT_3_CHANNELS
    
    outVec = (colorVec + brightness) * contrast
    
    # Clamp every color chanel
    for i in range(0, len(outVec)):
        if (outVec[i] > 255):
            outVec[i] = 255
        elif (outVec[i] < 0):
            outVec[i] = 0
    
    return outVec
        

minBright = 255
maxBright = 0

minVec = np.array([255, 255, 255])
maxVec = np.array([0, 0, 0])

minMean = 255
maxMean = 0

def clamp(val, minVal, maxVal):
    out = val;
    if (out > maxVal):
        out = maxVal
    elif (out < minVal):
        out = minVal
    
    return out

def clampVec(vec, minVal, maxVal):
    for i in range(0, len(vec)):
        if (vec[i] > maxVal):
            vec[i] = maxVal
        elif (vec[i] < minVal):
            vec[i] = minVal
    
    return vec

def desafio2(grayPixelVal, minBright, maxBright):
    conf.outImgChannels = conf.OUT_1_CHANNEL    
    b = -1*minBright;
    out = (grayPixelVal + b)*(255/(maxBright+b))
    
    return clamp(out, 0, 255)

def desafio3(colVec, minVec, maxVec):
    conf.outImgChannels = conf.OUT_3_CHANNELS
    b = -1*minVec
    out = (colVec + b) / (255/(maxBright+b))
    return clampVec(out, 0, 255)
    

while (True):
    # Getting the min and max brights
    for i in range(0, height):
        for j in range(0, width):
            # Min and max for grayscale
            brightVal = img_original_grayscale.item(i, j)
            
            # Finding the min bright value
            if (brightVal < minBright):
                minBright = brightVal
            
            if (brightVal > maxBright):
                maxBright = brightVal
                
            # Min and max for color image
            b0 = img_original.item(i, j, 0)
            g0 = img_original.item(i, j, 1)
            r0 = img_original.item(i, j, 2)
            originalColorVector = np.array([r0, g0, b0])
            # Check min and max for each channel
            for i in range(0, 3):
                if (originalColorVector[i] < minVec[i]):
                    minVec[i] = originalColorVector[i]
                
                if (originalColorVector[i] > maxVec[i]):
                    maxVec[i] = originalColorVector[i]
            
            
            # Min and max for mean image
            meanOfPixel = grayScaleShader(originalColorVector, conf.OUT_1_CHANNEL)
            if (meanOfPixel < minMean):
                minMean = meanOfPixel
            elif (meanOfPixel > maxMean):
                maxMean = meanOfPixel
                
    
    print("Min bright", str(minMean), "Max Brigt", str(maxMean));
    
    for i in range(0, height):
        for j in range(0, width):
            b0 = img_original.item(i, j, 0)
            g0 = img_original.item(i, j, 1)
            r0 = img_original.item(i, j, 2)
            
            brightVal = img_original_grayscale.item(i, j)
            
            originalColorVector = np.array([r0, g0, b0])
            ###################################
            ### Run here the shader program ###
            ###################################
            
            # Desafio 1
            # outColVector = grayScaleShader(originalColorVector, conf.OUT_1_CHANNEL)
            
            # Desafio 2
            #outColVector = desafio2(brightVal, minBright, maxBright)
            
            # Desafio 3
            # outColVector = desafio3(originalColorVector, minVec, maxVec);
            
            # Desafio 4
            '''
            Desafio 3 en la guia pasada
            O = (A + b)*a
            donde:
            b = -min
            a = 255/(max+b)
            
            Implementar el desafio 3 de la guia pasada
            En una imagen a color = la salida sera una imagen a color
            con base en el promedio = la imagen de entrada es un grayscale con promedio
            
            calcular el min y el max basado en el promedio
            '''
            outColVector = desafio3(originalColorVector, minMean, maxMean)
            
            #save output
            if (conf.outImgChannels == conf.OUT_3_CHANNELS):
                img_out_3_channels.itemset((i, j, 0), outColVector[2])
                img_out_3_channels.itemset((i, j, 1), outColVector[1])
                img_out_3_channels.itemset((i, j, 2), outColVector[0])
            elif (conf.outImgChannels == conf.OUT_1_CHANNEL):
                img_out_1_channel.itemset((i, j), outColVector)
            
    cv2.imshow("Original", img_original)
    
    if (conf.outImgChannels == conf.OUT_3_CHANNELS):
        cv2.imshow("Resultado", img_out_3_channels)
    elif (conf.outImgChannels == conf.OUT_1_CHANNEL):
        cv2.imshow("Resultado", img_out_1_channel)
    
    
    ch = 0xFF & cv2.waitKey()
    if (ch == ord('q') or ch == ord('Q')):
        if (conf.outImgChannels == conf.OUT_3_CHANNELS):
            cv2.imwrite("out_rgb.jpg", img_out_3_channels)
        elif (conf.outImgChannels == conf.OUT_1_CHANNEL):
            cv2.imwrite("out_1channel.jpg", img_out_1_channel)
        
        break
    
cv2.destroyAllWindows();
   