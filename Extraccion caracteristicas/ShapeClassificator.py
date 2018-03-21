# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 16:20:34 2018

@author: Jose Villalobos

This program, classifies an shape as the following classes:
    - Star
    - Circle
    - Square
"""

import numpy as np
import cv2
import sys # used for load the image

consoleApp = False;

if (consoleApp):
    img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE if (sys.argv[2] == '-b') else cv2.IMREAD_COLOR)
else:
    fileName = 'A6'
    img = cv2.imread('img/'+fileName+'.jpg', cv2.IMREAD_GRAYSCALE);




while(True):
    
    m = cv2.moments(img)
    
    area = m['m00'] # Area from moments, same as  cv2.contourArea()
    imgEdge = cv2.Canny(img, 100, 200) # Canny(img, minVal, maxVal) https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html
    
    # For better accuracy, use binary images. So before finding contours, apply threshold or canny edge detection.
    im, contourns, hierarchy = cv2.findContours(imgEdge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Get the contorn
    perimeter = cv2.arcLength(contourns[0], True) # Get the perimeter
    print('The perimeter is: ' + str(perimeter))
    centroidPos = (int(m['m10']/m['m00']), int(m['m01']/m['m00'])) # Centroid position
    
    # C Feature = perimeter**2 / Area
    c = (perimeter**2) / area
    print('The C feature is: ' + str(c))
    
    '''
    All the circles have a c feature aproximately equal to 0.05
    then, we can check if a shape is an circle with the following condition
    c < 0.06
    
    the C feature is aproximatelly equal to 0.063 for all the squares, then we can check if a shape is 
    an square with the following condition
    0.06 < c < 0.07
    
    The C feature is aproximatelly equal to 0.7 for all the stars, then we can check if a shape is an square
    with the following condition
    0.7 < c < 0.8
    '''
    if ( c < 0.06):
        # It is an circle
        print('Shape: circle')
    elif(0.06 < c < 0.07):
        # It is an square
        print('Shape: square')
    elif(0.7 < c < 0.8):
        # It is a star
        print('Shape: star')
    
    # TODO: Segment the bigger shape for do the calculttions (See example-image ./img/A7.jpg )
    
    
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.circle(img, centroidPos, 20, (0, 255, 0), thickness=-1) # Negative thickness means that a filled circle is to be drawn.
    img = cv2.drawContours(img, contourns, 0, (255, 0, 0), thickness=10) # Draws the contours in blue
    
    
    
    cv2.imshow("Canny", imgEdge)
    cv2.imshow('Image', img)
    
    ch = 0xFF & cv2.waitKey()
    if (ch == ord('q') or ch == ord('Q')):
        #cv2.imwrite("resultado.jpg", salida)
        break;
cv2.destroyAllWindows();