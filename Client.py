import cv2
import numpy
import socket
import struct
import sys
import time
import json
import gluoncv as gcv
import mxnet as mx
from XJBXX import RECV,SEND,Predict
from tennisdt import getqwq
from gluoncv import model_zoo, data, utils

HOST = '192.168.43.116'
PORT = 10000
buffSize = 655355
t = time.time()

def getFPS():
    global t
    sec = time.time() - t
    t = time.time()
    return 1/sec


net = gcv.model_zoo.get_model(
    'yolo3_mobilenet1.0_coco', pretrained=True, ctx=mx.gpu(0))
CAM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CAM.connect(('192.168.43.116', 10011))
DRI = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
DRI.connect(('192.168.43.116', 9920))
print('now waiting for frames...')
cnt = 0
x, y, r = 0, 0, 0
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
            Predict(net, imgdecode)
        img, x, y, r = getqwq(imgdecode)
        cv2.putText(img, "FPS={:.3} X={} Y={}".format(getFPS(), round(x), round(y)), (0, 240),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        cv2.imshow('frames', img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    except:
        continue
    
    msg = [{'x': x, 'y': y, 'r': r, 'key': key}]
    SEND(DRI, json.dumps(msg))
    #DRI.sendall(json.dumps(msg).encode('utf-8'))
DRI.close()
CAM.close()
cv2.destroyAllWindows()
