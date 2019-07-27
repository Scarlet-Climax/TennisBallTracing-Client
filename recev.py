import socket
import struct

HOST = ''
PORT = 1234

dataBuffer = bytes()
headerSize = 12

sn = 0


def dataHandle(headPack, body):
    global sn
    sn += 1
    print("%s's datapack" % sn)
    print("ver:%s, bodySize:%s, cmd:%s" % headPack)
    print(body.decode())
    print("")

def RECV(conn):
    global dataBuffer
    global headerSize
    #print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if data:
            dataBuffer += data
            while True:
                if len(dataBuffer) < headerSize:
                    break
                headPack = struct.unpack('!3I', dataBuffer[:headerSize])
                bodySize = headPack[1]
                if len(dataBuffer) < headerSize+bodySize:
                    break
                body = dataBuffer[headerSize:headerSize+bodySize]
                dataBuffer = dataBuffer[headerSize + bodySize :]
                return headPack,body

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                headPack,data = RECV(conn)
                dataHandle(headPack,data)
