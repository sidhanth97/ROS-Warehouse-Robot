#!/usr/bin/env python3

import numpy as np
import cv2
import argparse
import sys


ARUCO_DICT = {
 	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
 	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
 	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
 	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
 	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
 	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
 	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
 	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
 	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
 	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
 	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
 	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
 	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
 	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
 	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
 	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
 	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
 	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
 	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
 	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
 	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}


ar=cv2.imread('/home/manoj/project_5551/src/Marker4.png')
# cv2.imshow('Aruco',ar)
# cv2.waitKey(0)


arucoDict=cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(ar, arucoDict,parameters=arucoParams)

print(corners)

l=len(corners)
center=np.zeros((l,2))
i=0
while(i<l):
    center[i][0]=int((corners[i][0][0][0]+corners[i][0][2][0])/2)
    center[i][1]=int((corners[i][0][0][1]+corners[i][0][2][1])/2)
    i=i+1

# c=(247,244)
# c1=(11,9)
b=[255, 0, 0]
g=[0,0,255]
i=0
while i<l:
    cv2.circle(ar,(int(center[i][0]),int(center[i][1])),7,b, -1)
    cv2.putText(ar,str(ids[i]),((int(corners[i][0][0][0])+5),(int(corners[i][0][0][1])+10)),cv2.FONT_HERSHEY_SIMPLEX,0.75,g,3)
    i=i+1
# cv2.imshow('aruco',ar)
# cv2.waitKey(0)

k = np.reshape([643.5491628619162, 0.0, 540.5, 0.0, 643.5491628619162, 360.5, 0.0, 0.0, 1.0], (3,3))
obj_point = np.array([(0,0,0),(0.15,0,0),(0.15,0.15,0),(0.0,0.15,0)])
dist_coeff = np.zeros((4,1))
#dist_coeff = None
s, r, t = cv2.solvePnP(obj_point,corners[0], k, dist_coeff)
print( s ,r , t)

# cv2.circle(ar,(int(center[0][0]),int(center[0][1])),10,b, -1)
# cv2.circle(ar,(c1),10,b, -1)
# cv2.imshow('aruco',ar)
# cv2.waitKey(0)
