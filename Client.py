import cv2
import numpy
import socket
import struct
import sys
import time
import json
from tennisdt import getqwq

HOST = '192.168.1.108'
PORT = 10000
buffSize = 655355
t = time.time()


def getFPS():
    global t
    sec = time.time() - t
    t = time.time()
    return 1/sec


CAM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CAM.connect(('192.168.1.109', 10010))
DRI = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
DRI.connect(('192.168.1.109', 9920))
print('now waiting for frames...')
cnt = 0
x, y, r = 0, 0, 0
while True:
    #time.sleep(0.03)
    data, address = CAM.recvfrom(buffSize)
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
        img, x, y, r = getqwq(imgdecode)
        cv2.putText(img, "FPS={:.3} X={} Y={}".format(getFPS(),round(x),round(y)), (0, 240),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        cv2.imshow('frames', img)
        if (cnt % 5 == 0):
            cv2.imwrite('pic/{}.jpg'.format(cnt), imgdecode)
        key = cv2.waitKey(1)
        if key == 27:
            break
    except:
        continue
    msg = [{'x': x, 'y':y,'r':r,'key':key}]
    DRI.sendall(json.dumps(msg).encode('utf-8'))
DRI.close()
CAM.close()
cv2.destroyAllWindows()
