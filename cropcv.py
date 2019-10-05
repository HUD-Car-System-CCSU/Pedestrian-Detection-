import cv2
import numpy as np

image = cv2.imread("gtr.jpg")
cv2.imshow("original", image)

print (image.shape) #row,col,channels

Lframe1 = image[0:720, 0:400]
Cframe1 = image[0:720, 400:880]
Rframe1 = image[0:720,880:1280]

(h,w) = Lframe1.shape[:2]
center=(w/2,h/2)
M = cv2.getRotationMatrix2D(center, 180, 1.0)
Lframe1flip =  cv2.warpAffine(image[0:720, 0:400], M, (w,h))
 
putitback = np.concatenate((Lframe1flip,Cframe1, Rframe1), axis=1)
cv2.imshow('flipped',Lframe1flip)  
cv2.imshow('cropped',Rframe1)  
cv2.imshow('stitched',putitback)

cv2.waitKey(0)
cv2.destroyAllWindows()
