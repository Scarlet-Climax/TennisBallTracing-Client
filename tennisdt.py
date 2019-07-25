import numpy as np
import cv2
import time
import imutils

def getqwq(img):

    tennislower = (29, 86, 6)
    tennisupper = (64, 255, 255)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #print(hsv)
    mask = cv2.inRange(hsv, tennislower, tennisupper)
    cv2.imshow("mask", mask)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            cv2.circle(img, (int(x), int(y)), int(radius),
                            (0, 255, 255), 2)
            cv2.circle(img, center, 5, (0, 0, 255), -1)
        return img,x,y,radius
        #cv2.imshow("Frame", img)
    return img,-1,-1,-1


if __name__ == '__main__':
    
    img = cv2.imread("pic/50.jpg")
    cv2.imshow("Frame", getqwq(img))
    cv2.waitKey(10000)
    
