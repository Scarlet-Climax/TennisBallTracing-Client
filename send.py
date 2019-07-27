import socket
import time
import struct
import json


def SEND(client, body):
    ver = 1
    #body = json.dumps(dict(hello="world"))
    #print(body)
    cmd = 101
    header = [ver, body.__len__(), cmd]
    headPack = struct.pack("!3I", *header)
    sendData = headPack + body.encode()
    client.send(sendData)
    
