import cv2
import numpy
import socket
import struct

HOST='192.168.1.104'
PORT=10000
buffSize=65535

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((HOST,PORT))
print('now waiting for frames...')
while True:
    data,address=server.recvfrom(buffSize)
    if len(data)==1 and data[0]==1: 
        server.close()
        cv2.destroyAllWindows()
        exit()
    try:
        data=bytearray(data)
        print('have received one frame')
        data=numpy.array(data)
        imgdecode=cv2.imdecode(data,1)
        cv2.imshow('frames',imgdecode)
        if cv2.waitKey(1)==27:
            break
    except:
        continue

server.close()
cv2.destroyAllWindows()