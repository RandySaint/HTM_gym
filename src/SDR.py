# Class for SDR data structure

import numpy as np
import random

class SDR(object):
    def __init__(self, size=1, pct=0.0, meta={}):
        self.size = size
        self.sdr = np.zeros(size, dtype=np.uint64)
        self.meta = meta
        if pct > 0.0:
            self.randomlyInitialize(pct)

    def randomlyInitialize(self, pct=0.5):
        # randomly set pct bits
        for i in range(self.size):
            for j in range(64):
                if random.random() <= pct:
                    self.sdr[i] = self.sdr[i] | np.uint64(1 << j)

    def get(self, row, col):
        # get the bit state at row, col
        ret = False
        if (self.sdr[row] & np.uint64(0x1 << col)) != 0:
            ret = True
        return ret

    def setRow(self, row, val):
        # set a 1 row SDR
        self.sdr[row] = val

    def setBit(self, row, col):
        # row must be < size
        # col must be < 64
        self.sdr[row] = self.sdr[row] | np.uint64(0x1 << col)

    def clearBit(self, row, col):
        # row must be < size
        # col must be < 64
        self.sdr[row] = self.sdr[row] & ~np.uint64(1 << col)

    def getSize(self):
        return self.size

    def popcount(self, bits):
        bits = (bits & np.uint64(0x5555555555555555)) + (np.uint64(bits & np.uint64(0xAAAAAAAAAAAAAAAA)) >> np.uint64(1))
        bits = (bits & np.uint64(0x3333333333333333)) + (np.uint64(bits & np.uint64(0xCCCCCCCCCCCCCCCC)) >> np.uint64(2))
        bits = (bits & np.uint64(0x0F0F0F0F0F0F0F0F)) + (np.uint64(bits & np.uint64(0xF0F0F0F0F0F0F0F0)) >> np.uint64(4))
        bits = (bits & np.uint64(0x00FF00FF00FF00FF)) + (np.uint64(bits & np.uint64(0xFF00FF00FF00FF00)) >> np.uint64(8))
        bits = (bits & np.uint64(0x0000FFFF0000FFFF)) + (np.uint64(bits & np.uint64(0xFFFF0000FFFF0000)) >> np.uint64(16))
        bits = (bits & np.uint64(0x00000000FFFFFFFF)) + (np.uint64(bits & np.uint64(0xFFFFFFFF00000000)) >> np.uint64(32))
        return np.int(bits)
    

    def getOverlap(self, other):
        # if sizes different, fail
        overlap = 0
        for i in range(self.size):
            overlap += self.popcount(self.sdr[i] & other.getRow(i))
        return overlap

    def concatenate(self, other):
        # merge 2 SDRs and return new SDR
        newOne = SDR(self.size + other.size)
        for i in range(self.size):
            newOne.setRow(i, self.getRow(i))
        for i in range(other.size):
            newOne.setRow(i+self.size, other.getRow(i))
        return newOne

    def getRow(self, row):
        # row must be less than size
        return self.sdr[row]

    def pr(self):
        # print self.meta
        for i in range(self.size):
            st = ""
            for j in range(64):
                if self.sdr[i] & np.uint64(1 << j) > 0:
                    st += "1"
                else:
                    st += "."
            print st


if __name__ == "__main__":
    # run test
    test = SDR(4)
    test.pr()
    test.setBit(0,16)
    test.pr()
    print ("Overlap=", test.getOverlap(test))
    test.clearBit(0,16)
    test.randomlyInitialize(0.2)
    test.pr()
    print ("Overlap=", test.getOverlap(test))


