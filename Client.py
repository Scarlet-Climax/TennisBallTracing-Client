import cv2
import numpy
import socket
import struct
import sys
import time
import json
GPU = 0
if GPU==1:
    import gluoncv as gcv
    import mxnet as mx
    from gluoncv import model_zoo, data, utils
from XJBXX import RECV,SEND,Predict
from tennisdt import getqwq

#HOST = '169.254.189.95'
HOST = "192.168.43.116"
PORT = 10000
buffSize = 655355
t = time.time()

def getFPS():
    global t
    sec = time.time() - t
    t = time.time()
    return 1/sec
def nothing(x):
    pass

net = gcv.model_zoo.get_model(
        'yolo3_mobilenet1.0_coco', pretrained=True, ctx=mx.gpu(0)) if GPU==1 else 0
CAM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CAM.connect((HOST, 10011))
DRI = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
DRI.connect((HOST, 9920))
print('now waiting for frames...')
cnt = 0
x, y, r = 0, 0, 0
cv2.namedWindow("frames")
cv2.createTrackbar("a", "frames", 0, 300, nothing)
cv2.createTrackbar("b", "frames", 0, 510, nothing)
while True:
    #time.sleep(0.03)
    header,data=RECV(CAM)
    #data= CAM.recv(buffSize)
    cnt = cnt + 1
    key=-1
    if len(data) == 1 and data[0] == 1:
        CAM.close()
        DRI.close()
        cv2.destroyAllWindows()
        exit()
    try:
        data = bytearray(data)
        data = numpy.array(data)
        imgdecode = cv2.imdecode(data, 1)
        if (cnt % 5 == 0):
            #cv2.imwrite('pic/{}.jpg'.format(cnt), imgdecode)
            #cv2.imwrite('new.jpg'.format(cnt), imgdecode)
            if GPU == 1:
                Predict(net, imgdecode)
            pass
        img, x, y, r = getqwq(imgdecode)
        if GPU==0:
            cv2.putText(img, "FPS={:.3} X={} Y={}".format(getFPS(), round(x), round(y)), (0, 240),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            cv2.imshow('frames', img)
        else:
            pass
        key = cv2.waitKey(20 if GPU==1 else 35)
        if key == 27:
            break
    except:
        continue
    
    msg = [{'x': x, 'y': y, 'r': r, 'key': key,'time':time.time()}]
    print(json.dumps(msg))
    SEND(DRI, json.dumps(msg))
    #DRI.sendall(json.dumps(msg).encode('utf-8'))
DRI.close()
CAM.close()
cv2.destroyAllWindows()
