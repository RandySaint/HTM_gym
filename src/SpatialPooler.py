#Spatial Pooler
from SDR import SDR
from PermanenceArray import PermanenceArray
from Encoder import Encoder
import numpy as np
import random

class SpatialPooler(object):
    def __init__(self, size):
        # initialize basic stuff here
        self.size = size
        self.columns = SDR(size)

    def initialize(self, inputSize, inputDefinition):
        # inputSize - number of separate inputs for this SP
        # inputDefinition - list of tuples (name, width, low, high)
        # each cell in SP (64xSize) gets a connection matrix to the Input
        self.inputSize = inputSize
        # connections are an SDR for each column with random connections to 50% of the inputs
        self.connections = [[SDR(inputSize,0.5) for j in range(64)] for i in range(self.size)]
        # pa is the permanence of each of the connections to the inputs
        self.pa = [[PermanenceArray(self.connections[i][j]) for j in range(64)] for i in range(self.size)]
        # create an array for adding boost
        self.boost = np.zeros((self.size, 64))
        self.encoders = []
        self.names = []
        for i in range(inputSize):
            name,w,l,h = inputDefinition[i]
            self.encoders.append(Encoder(width=w,low=l,high=h))
            self.names.append(name)
        self.inputSDR = SDR(self.inputSize)

    def createInput(self,inputValues):
        # inputValues is array of values in order of initialized
        for i in range(self.inputSize):
            self.inputSDR.setRow(i,self.encoders[i].encode(inputValues[i]))

    def compute(self):
        # Input SDR size must match self.inputSize
        # create an array for summations
        arr = np.zeros((self.size, 64))
        # for each cell check overlapp of permanence array
        cut = 0
        for i in range(self.size):
            for j in range(64):
                # could factor (divide) boost here
                arr[i][j] = self.pa[i][j].checkOverlap(self.inputSDR) + int(self.boost[i][j])
                #arr[i][j] = self.pa[i][j].checkOverlap(inputSDR)
                cut = max(cut, arr[i][j])
                self.boost[i][j] += 1
        # find cutoff for top 2-4% (tunable?)
        threepct = self.size * 2 # 2/64 = 3%
        cut -= 1
        count = np.count_nonzero(arr>cut)
        #print("cut=",cut,"count=",count)
        while count < threepct:
            cut -=1
            count = np.count_nonzero(arr>cut)
            #print("cut=",cut,"count=",count)

        # create output SDR with summations that exceed cutoff
        ret = SDR(self.size)
        for i in range(self.size):
            for j in range(64):
                if arr[i][j] > cut:
                    # learning code
                    #self.prPA(i,j)
                    self.pa[i][j].updatePermanence(self.inputSDR)
                    #self.prPA(i,j)
                    # done learning, set the bit
                    ret.setBit(i,j)
                    self.boost[i][j] = 0
        return ret

    def whatValue(self, testSDR, gets):
        # gets is list of indexes of which values to get
        # return array of values
        # build an testInput SDR by reverse engineering 
        print ""
        # create an empty testInput
        testInput = SDR(self.inputSize)
        testArray = np.zeros((self.inputSize,64))
        # for each on bit in the testSDR, increment the values in TestInput that correspond to the permanence>threshold inputs
        for i in range(self.size):
            for j in range(64):
                if testSDR.get(i,j):
                    self.pa[i][j].pushTo(testArray)
        for i in range(self.inputSize):
            st = ""
            for j in range(64):
                st += str(min(9, int(testArray[i][j])))
            print st
        #testInput.pr()

        

    def prConn(self, r, c):
        self.connections[r][c].pr()
    def prPA(self, r, c):
        self.pa[r][c].pr()



    #def feedforward(inputs):
        # should 

if __name__ == "__main__":
    # run test
    test = SpatialPooler(7) # internally 7 rows
    test.initialize(4,(("pos",16,0,10),("pdot",16,0,10),("theta",16,0,10),("tdot",16,0,10))) # input has 4 rows
    test.prConn(2,32)
    test.prPA(2,32)
    
    test.createInput((4,1,6,10))
    save = test.compute()
    for i in range(10):
        test.createInput((random.uniform(0,10),random.uniform(0,10),random.uniform(0,10),random.uniform(0,10)))
        print ""
        #test.inputSDR.pr()
        out = test.compute()
        out.pr()

    test.createInput((4,1,6,10))
    test.inputSDR.pr()
    out = test.compute()
    print "final out (4,1,6,10)"
    out.pr()
    print "first out (4,1,6,10)"
    save.pr()
    test.whatValue(out,(0))

