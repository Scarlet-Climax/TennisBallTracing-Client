import socket
import struct
import json
from gluoncv import model_zoo, data, utils
import cv2
import gluoncv as gcv
import mxnet as mx
from matplotlib import pyplot as plt
import random

def cv_plot_bbox(img, bboxes, scores=None, labels=None, thresh=0.5,
                 class_names=None, colors=None,
                 absolute_coordinates=True, scale=1.0):
    from matplotlib import pyplot as plt

    if labels is not None and not len(bboxes) == len(labels):
        raise ValueError('The length of labels and bboxes mismatch, {} vs {}'
                         .format(len(labels), len(bboxes)))
    if scores is not None and not len(bboxes) == len(scores):
        raise ValueError('The length of scores and bboxes mismatch, {} vs {}'
                         .format(len(scores), len(bboxes)))

    if isinstance(img, mx.nd.NDArray):
        img = img.asnumpy()
    if isinstance(bboxes, mx.nd.NDArray):
        bboxes = bboxes.asnumpy()
    if isinstance(labels, mx.nd.NDArray):
        labels = labels.asnumpy()
    if isinstance(scores, mx.nd.NDArray):
        scores = scores.asnumpy()
    if len(bboxes) < 1:
        return img
    if not absolute_coordinates:
        # convert to absolute coordinates using image shape
        height = img.shape[0]
        width = img.shape[1]
        bboxes[:, (0, 2)] *= width
        bboxes[:, (1, 3)] *= height
    else:
        bboxes *= scale
    # use random colors if None is provided
    if colors is None:
        colors = dict()
    for i, bbox in enumerate(bboxes):
        if scores is not None and scores.flat[i] < thresh:
            continue
        if labels is not None and labels.flat[i] < 0:
            continue
        cls_id = int(labels.flat[i]) if labels is not None else -1
        if cls_id not in colors:
            if class_names is not None:
                colors[cls_id] = plt.get_cmap('hsv')(cls_id / len(class_names))
            else:
                colors[cls_id] = (
                    random.random(), random.random(), random.random())
        xmin, ymin, xmax, ymax = [int(x) for x in bbox]
        bcolor = [x * 255 for x in colors[cls_id]]
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), bcolor, 2)
        if class_names is not None and cls_id < len(class_names):
            class_name = class_names[cls_id]
        else:
            class_name = str(cls_id) if cls_id >= 0 else ''
        score = '{:d}%'.format(
            int(scores.flat[i]*100)) if scores is not None else ''
        if class_name or score:
            y = ymin - 15 if ymin - 15 > 15 else ymin + 15
            cv2.putText(img, '{:s} {:s}'.format(class_name, score),
                        (xmin, y), cv2.FONT_HERSHEY_SIMPLEX, min(scale/2, 2),
                        bcolor, min(int(scale), 5), lineType=cv2.LINE_AA)
    return img

def Predict(net,frame):

    # Image pre-processing
    frame = mx.nd.array(frame).astype('uint8')
    rgb_nd, frame = gcv.data.transforms.presets.ssd.transform_test(
        frame, short=512, max_size=700)

    # Run frame through network
    class_IDs, scores, bounding_boxes = net(rgb_nd.as_in_context(mx.gpu(0)))

    # Display the result
    img = cv_plot_bbox(
        frame, bounding_boxes[0], scores[0], class_IDs[0], class_names=net.classes)
    cv2.imshow("predict",img)
    cv2.waitKey(1)


dataBuffer = bytes()
headerSize = 12

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
                dataBuffer = dataBuffer[headerSize + bodySize:]
                return headPack, body


def SEND(client, body):
    ver = 1
    #body = json.dumps(dict(hello="world"))
    #print(body)
    cmd = 101
    header = [ver, body.__len__(), cmd]
    headPack = struct.pack("!3I", *header)
    sendData = headPack + body.encode('utf-8')
    client.sendall(sendData)

