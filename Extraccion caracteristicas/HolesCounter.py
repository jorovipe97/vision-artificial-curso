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
    fileName = 'C2'
    img = cv2.imread('img/'+fileName+'.png', cv2.IMREAD_COLOR);


NONE = -1
CIRCLE = 0;
SQUARE = 1;
STAR = 2;

shapeClass = NONE

while(True):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    m = cv2.moments(img)
      
    area = m['m00'] # Area from moments, same as  cv2.contourArea()
    imgEdge = cv2.Canny(img, 200, 220) # Canny(img, minVal, maxVal) https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html
    
    # Tutorial about contourn hirarchy (the second argument) https://docs.opencv.org/3.4.0/d9/d8b/tutorial_py_contours_hierarchy.html
    # For better accuracy, use binary images. So before finding contours, apply threshold or canny edge detection.
    im, contourns, hierarchy = cv2.findContours(imgEdge, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE) # Get the contorn
    cv2.imshow('B ', im)
    print(hierarchy)
    
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for i in range(len(contourns)):
        print('\nShape ' + str(i+1))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        perimeter = cv2.arcLength(contourns[i], True) # Get the perimeter
        print('The perimeter is: ' + str(perimeter))
        centroidPos = (int(m['m10']/m['m00']), int(m['m01']/m['m00'])) # Centroid position
        
        # C Feature = perimeter**2 / Area
        c = (perimeter**2) / area
        print('The C feature is: ' + str(c))
        
        
        # TODO: Segment the bigger shape for do the calculttions (See example-image ./img/A7.jpg )
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = cv2.circle(img, centroidPos, 3, (0, 255, 0), thickness=-1) # Negative thickness means that a filled circle is to be drawn.
        img = cv2.drawContours(img, contourns, i, (255, 0, 0), thickness=2) # Draws the contours in blue

    # Findo contourns is selecting inner an outter contourns then we dont need that, then we need to substract the parent contourn
    print('\nHole count: ' + str(int((len(contourns)/2)-1)))
    
    cv2.imshow("Canny", imgEdge)
    cv2.imshow('Image', img)
    
    ch = 0xFF & cv2.waitKey()
    if (ch == ord('q') or ch == ord('Q')):
        #cv2.imwrite("resultado.jpg", salida)
        break;
cv2.destroyAllWindows();