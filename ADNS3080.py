import spidev
import RPi.GPIO as GPIO
import time 

pin_rst = 22

class ADNS3080():
    def readReg(self, address):
        result = self.spi.xfer([address, 0], 100)
        return result[1]
    
    def writeReg(self, address, data):
        self.spi.xfer([address, data], 100)

    def __init__(self, rstpin=22, bus=0, device=0):
        self.rstpin = rstpin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(rstpin, GPIO.OUT)
        GPIO.output(rstpin, GPIO.LOW)
        self.spi = spidev.SpiDev()
        self.spi.mode = 3
        self.spi.open(bus, device)

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
        if self.readReg(0) != 23:
            print "ERROR: Expected device ID 0x17, got 0x%x."
            return
        print "SROM ID:", self.readReg(0x1f)


if __name__ == "__main__":
    this = ADNS3080()
    this.wait()
    this.initializeSensor()
