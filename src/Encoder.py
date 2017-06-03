# Class for a scalar Encoder

import numpy as np
import SDR

# Maybe 64 bits is too wide for some values
# want some overlap, and no bits should always be on
class Encoder(object):
    def __init__(self, width, low, high):
        self.width = width # number of bits (of 64 to set)
        self.play = 64 - width
        self.bits = 0
        for i in range(self.width):
            self.bits = (self.bits << 1) | 1
        self.low = low
        self.high = high
        # assumes high > low 
        self.range = high - low

    def encode(self, val):
        pct = (self.play*(min(max(val,self.low),self.high)-self.low))/self.range
        djks = self.bits << int(pct)
        return djks
        

if __name__ == "__main__":
    # run test
    tenc = Encoder(32, 100, 110)
    print bin(tenc.encode(99))
    print bin(tenc.encode(100))
    print bin(tenc.encode(102))
    print bin(tenc.encode(103))
    print bin(tenc.encode(104))
    print bin(tenc.encode(110))
    print bin(tenc.encode(111))
    print bin(tenc.encode(120))
    print bin(tenc.encode(130))
