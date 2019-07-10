import cv2
img = cv2.imread('pic/265.jpg')
height, width = img.shape[:2]

HSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

def getposHsv(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print("HSV is",HSV[y,x])
def getposBgr(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print("Bgr is",img[y,x])

cv2.imshow("imageHSV",HSV)
cv2.imshow('image',img)
cv2.setMouseCallback("imageHSV",getposHsv)
cv2.setMouseCallback("image",getposBgr)
cv2.waitKey(0)