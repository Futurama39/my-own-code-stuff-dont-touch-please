import matplotlib
import numpy as np
import cv2

img = cv2.imread(r"F:/BFB/102323.jpg")   
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
kernel2 = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,10))
imgp = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
#cv2.imshow('image',imgp)
#cv2.waitKey(0)

#img2 = cv2.fastNlMeansDenoisingColored(img,None,10,10,61,40)

#img3 = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)

img3 = cv2.dilate(img,kernel2,iterations=120)
#img3 = cv2.erode(img3,kernel3,iterations=10)
#img3 = cv2.morphologyEx(img3,cv2.MORPH_GRADIENT,kernel)

cv2.imshow('image',img3)
#cv2.imshow('image',img2)
cv2.waitKey(0)