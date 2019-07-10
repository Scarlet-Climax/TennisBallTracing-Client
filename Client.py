import cv2
import numpy
import socket
import struct
import sys
from tennisdt import getqwq

HOST = '192.168.1.104'
PORT = 10000
buffSize = 65535

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))
print('now waiting for frames...')
cnt = 0
x,y,r=0,0,0
while True:
    data, address = server.recvfrom(buffSize)
    server.sendall('Good: x:{:3f} y:{:3f} r:{:3f}\r'.format(x,y,r).encode('utf-8'))
    cnt = cnt+1
    if len(data) == 1 and data[0] == 1:
        server.close()
        cv2.destroyAllWindows()
        exit()
    try:
        data = bytearray(data)
        print('received one frame')
        data = numpy.array(data)
        imgdecode = cv2.imdecode(data, 1)
        img,x,y,r=getqwq(imgdecode)
        cv2.imshow('frames', img)
        if (cnt % 5 == 0):
            cv2.imwrite('pic/{}.jpg'.format(cnt), imgdecode)
        if cv2.waitKey(1) == 27:
            break
    except:
        continue
    
server.close()
cv2.destroyAllWindows()
