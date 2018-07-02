import spidev 
import RPi.GPIO as GPIO 
import time 
import adns3080_srom as srom

class ADNS3080():
    def readReg(self, address):
        result = self.spi.xfer2([address, 0], 1000000, 100)
        return result[1]
    
    def writeReg(self, address, data):
        address = address | 0b10000000
        self.spi.xfer2([address, data], 1000000, 100)

    def __init__(self, rstpin=22, bus=0, device=0):
        self.rstpin = rstpin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(rstpin, GPIO.OUT)
        GPIO.output(rstpin, GPIO.LOW)
        self.spi = spidev.SpiDev()
        self.spi.mode = 3
        #self.spi.max_speed_hz = 1953000
        self.spi.open(bus, device)
        
    def downloadSROM(self, SROM):
        GPIO.output(self.rstpin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.rstpin, GPIO.LOW)
        time.sleep(0.1)
        self.writeReg(0x20, 0x44)
        self.writeReg(0x23, 0x07)
        self.writeReg(0x24, 0x88)
        time.sleep(0.1)
        self.writeReg(0x14, 0x18)
        self.spi.xfer2([0x60]+SROM, 1000000, 100)
        time.sleep(1)
        print "SROM ID:", self.readReg(0x1f)

    def wait(self):
        #catches an inevitable "Bad file descriptor"
        try:
            time.sleep(2)
        except:
            pass

    def initializeSensor(self):
        #Toggle reset
        GPIO.output(self.rstpin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.rstpin, GPIO.LOW)
        time.sleep(0.1)
        id = self.readReg(0)
        id = self.readReg(0)
        if id != 23:
            print "ERROR: Expected device ID 0x17, got 0x%x."%id
            return
        print "SROM ID:", self.readReg(0x1f)

    def runSelfTest(self):
        GPIO.output(self.rstpin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.rstpin, GPIO.LOW)
        time.sleep(0.1)
        currentRegVal = self.readReg(0x0a)
        self.writeReg(0x0a, currentRegVal | 0b00100000)
        time.sleep(2.)
        print "%x, %x"%(self.readReg(0x0d), self.readReg(0x0c))

    def frameCapture(self):
        self.writeReg(0x13, 0x83)
        time.sleep(0.1)
        outputData = self.spi.xfer([0x40]+[0]*900, 1000000, 100)
        outputData = outputData[1:]
        for i, byte in enumerate(outputData):
            if (byte & 0b10000000) == 0:
                print "WARNING: MSB of byte %d not set."%i
            if (byte & 0b01000000) == 0:
                if i == 0:
                    print "WARNING: Bit 6 of first byte of frame data not set."
            else:
                if i > 0:
                    print "WARNING: Bit 6 of byte %d of frame data is set."%i
            outputData[i] = byte & 0b01111111
        return outputData
        
        

if __name__ == "__main__":
    this = ADNS3080()
    this.wait()
    this.initializeSensor()
    #this.downloadSROM(srom.srom)
    print this.frameCapture()
    #while(1):
        #print format(this.readReg(2), '#010b'), this.readReg(5),  this.readReg(3), this.readReg(4)
