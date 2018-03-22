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
    fileName = 'B1'
    img = cv2.imread('img/'+fileName+'.jpg', cv2.IMREAD_COLOR);


NONE = -1
CIRCLE = 0;
SQUARE = 1;
STAR = 2;

shapeClass = NONE

while(True):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    m = cv2.moments(img)
    
    
    area = m['m00'] # Area from moments, same as  cv2.contourArea()
    
    # Extract noise from the image
    img = cv2.GaussianBlur(img, (5, 5), 2)
    cv2.imshow('Threshold', img)
    
    #img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    imgEdge = cv2.Canny(img, 100, 200) # Canny(img, minVal, maxVal) https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html
    
    # Contourn feature
    # For better accuracy, use binary images. So before finding contours, apply threshold or canny edge detection.
    im, contourns, hierarchy = cv2.findContours(imgEdge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Get the contorn
    
    print(len(contourns))
    
    # Converts here for avoid error in the first iteratoin of the for loop
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for i in range(len(contourns)):
        print('\nShape ' + str(i+1))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Perimeter feature
        perimeter = cv2.arcLength(contourns[i], True) # Get the perimeter
        print('The perimeter is: ' + str(perimeter))
        
        # Centroid feature
        x = int(m['m10']/m['m00'])
        y = int(m['m01']/m['m00'])
        centroidPos = (x, y) # Centroid position
        centroidPosArr = np.array([[x, y]])
        
        # C Feature = perimeter**2 / Area
        c = (perimeter**2) / area
        print('The C feature is: ' + str(c))
        
        
        
        # standard deviation feature
        radialLengths = []
        # Iterates all the contourn's points
        for j in range(len(contourns[i])):
            # Save to the radialLengths array: (contourn_point) - (centroid)
            diff = (contourns[i][j]) - (centroidPosArr)
            # Computes the lenthg of the vectors
            length = np.linalg.norm(diff[0])
            
            
            radialLengths.append(length)
            #print(contourns[i][j] )        
        # Computes the standard deviation
        stdDev = np.std(np.array(radialLengths, np.float32))        
        print('Standard deviation: ' + str(stdDev))
        
        '''
        In this classifier we look that the standard deviaton of the radial lengths (contourn point[j] - centroid)
        are aproximatelly equal to 0 (zero) when the shape is an circle
        '''        
        if (stdDev < 1.1):
            print('Shape: circle (Or ellipse with closed focus')
        else:
            print('Shape: Square (Or other)')
        
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = cv2.circle(img, centroidPos, 3, (0, 255, 0), thickness=-1) # Negative thickness means that a filled circle is to be drawn.
        img = cv2.drawContours(img, contourns, i, (255, 0, 0), thickness=10) # Draws the contours in blue
                
    cv2.imshow("Canny", imgEdge)
    cv2.imshow('Image', img)
    
    ch = 0xFF & cv2.waitKey()
    if (ch == ord('q') or ch == ord('Q')):
        #cv2.imwrite("resultado.jpg", salida)
        break;
cv2.destroyAllWindows();