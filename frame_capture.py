import ADNS3080
import matplotlib.pyplot as plt
import numpy as np
import time
import array
import socket

#Set to local IP
TCP_IP = '192.168.1.27'

TCP_PORT = 8000
BUFFER_SIZE = 60  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr


startTime = time.time()
this = ADNS3080.ADNS3080()
this.wait()
this.initializeSensor()
initTime = time.time()

while 1:
    try:
        rawdata = this.frameCapture()
        #capTime = time.time()
        print "Got data..."
        conn.send(array.array('B', rawdata).tostring())
    except:
        conn.close() 
        raise

#reshapedData = np.reshape(rawdata, (30,30))[::-1,::-1]
#reshTime = time.time()
#plt.imshow(reshapedData, interpolation="none")
#plotTime = time.time()
#print "Initialization time:", initTime-startTime
#print "Capture time:", capTime-initTime
#print "Reshape time:", reshTime - capTime
#print "Display time:", plotTime - reshTime
#plt.show()

conn.close()
