import ADNS3080
import matplotlib.pyplot as plt
import numpy as np
import time

startTime = time.time()
this = ADNS3080.ADNS3080()
this.wait()
this.initializeSensor()
initTime = time.time()
rawdata = this.frameCapture()
capTime = time.time()
print "Got data..."
reshapedData = np.reshape(rawdata, (30,30))[::-1,::-1]
reshTime = time.time()
plt.imshow(reshapedData, interpolation="none")
plotTime = time.time()
print "Initialization time:", initTime-startTime
print "Capture time:", capTime-initTime
print "Reshape time:", reshTime - capTime
print "Display time:", plotTime - reshTime
plt.show()

