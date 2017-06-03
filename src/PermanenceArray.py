# class for Array of Permanence valueso
import numpy as np
import random
from SDR import SDR

class PermanenceArray(object):
    def __init__(self, sdr):
        self.threshold = 64
        self.size = sdr.size
        self.pa = np.zeros((self.size,64),dtype=np.uint8)
        self.on = SDR(self.size)
        for i in range(self.size):
            for j in range(64):
                if sdr.get(i, j):
                    self.pa[i][j] = random.uniform(1,255)
                    if (self.pa[i][j] > self.threshold):
                        self.on.setBit(i,j)

    def updatePermanence(self, inputSDR):
        for i in range(self.size):
            for j in range(64):
                if self.pa[i][j] > 0:
                    # have a permanence here check against input
                    if inputSDR.get(i, j):
                        # we have a match, strengthen = default value 2
                        self.pa[i][j] = min(255, self.pa[i][j]+2)
                        if (self.pa[i][j] > self.threshold):
                            self.on.setBit(i,j)
                    else:
                        # no match, decrement = default value 1
                        self.pa[i][j] = max(1, self.pa[i][j]-1)
                        if (self.pa[i][j] < self.threshold):
                            self.on.clearBit(i,j)
    
    def updateOn(self):
        for i in range(self.size):
            for j in range(64):
                if (self.pa[i][j] > self.threshold):
                    self.on.setBit(i,j)
                else:
                    self.on.clearBit(i,j)


    def checkOverlap(self, inputSDR):
        # assumes SDR sizes are the same
        return self.on.getOverlap(inputSDR)

    def setThreshold(self, thresh): # thresh in 0.0 to 1.0 range
        self.threshold = np.uint8(thresh*256.0)

    def pushTo(self, testArray):
        for i in range(self.size):
            for j in range(64):
                if self.pa[i][j] > self.threshold:
                    testArray[i][j] += 1

    def pr(self):
        for i in range(self.size):
            st = ""
            for j in range(64):
                if (self.pa[i][j] > 0):
                    st += str((10*self.pa[i][j])/256)
                else:
                    st += "."
            print st

if __name__ == "__main__":
    # run test
    sdr = SDR(4)
    sdr.randomlyInitialize(0.25)
    test = PermanenceArray(sdr)
    #test.init(sdr)
    print("25% random weights")
    test.pr()
    print("SDR above threshold ",test.threshold)
    test.on.pr()
