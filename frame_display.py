import socket
import matplotlib.pyplot as plt
import numpy as np
import array

TCP_IP = '47.41.14.152'
TCP_PORT = 8001
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

reshapedData = [[0]*30]*30
plot = plt.imshow(reshapedData, interpolation="none")
plt.ion()
plt.show()

while True:
    try:
        datastr = s.recv(900)
        if len(datastr) == 900:
            print "Got data"
            #print datastr
            rawdata = array.array('B')
            rawdata.fromstring(datastr)
            rawdata = list(rawdata)
            #print "rawdata:"
            #print rawdata
            reshapedData = np.reshape(rawdata, (30,30))[::-1,::-1]
            #print "reshaed data:"
            #print reshapedData
            plot.set_data(reshapedData)
            plot.autoscale()
            plt.draw()
            plt.pause(0.001)
    except:
        s.close()
        raise
