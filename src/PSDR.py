# Class for PSDR data structure (Permanence Weighted SDR)
# Major data structures:
# Height, Width, Size(H*W)
# Permanence List of Tuples (ID# of field linked to, permanence of link (0-255) ) - /* Future perm can fit in byte for compact C implementation */
# Threshold - ID#s with permanence greater than Threshold will be stored in an SDRL
# SDRL will be stored as a 1 dimensional list of numbers, indicating where bits are set to 1

import numpy as np
import random

class SDRL(object):
    def __init__(self, height=1, width=1, pct=0.0, meta={}):
        self.height = height
        self.width = width
        self.size = height * width
        self.sdr = set()
        self.meta = meta
        if pct > 0.0:
            self.randomlyInitialize(pct)

    def randomlyInitialize(self, pct=0.5):
        # randomly set pct bits
        for i in range(self.size):
            for j in range(64):
                if random.random() <= pct:
                    self.sdr[i] = self.sdr[i] | np.uint64(1 << j)

    def get(self, pos):
        # get the bit state at pos
        # if the pos value is in the list 
        return if pos in self.sdr

    def get(self, row, col):
        # get the bit state at row, col
        return self.get(row*width + col)

    def setBit(self, pos):
        # simply add this pos to the list
        self.sdr.update(pos)

    def setBit(self, row, col):
        # col must be < 64
        self.setBit(row*width + col)

    def clearBit(self, pos):
        # col must be < 64
        self.sdr.discard(pos)

    def clearBit(self, row, col):
        # col must be < 64
        self.sdr[row] = self.sdr[row] & ~np.uint64(1 << col)

    def getSize(self):
        return self.size

    def getOverlap(self, other):
        # if sizes different, fail
        return len(self.sdr.intersection(other.sdr))

    def concatenate(self, other):
        # merge 2 SDRs and return new SDR
        return self.sdr.union(other.sdr)

    def pr(self):
        # print self.meta
        for i in range(self.height):
            st = ""
            for j in range(self.width):
                if self.getBit(i,j)
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
