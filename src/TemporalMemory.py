# class for Temporal Memory

from Synapse import Synapse
from Cell import Cell
from SDR import SDR
from PermanenceArray import PermanenceArray
import numpy as np
import random

class TemporalMemory(object):
    def __init__(self,size,depth=8,segments=1):
        # initialize basic stuff here
        self.size = size
        self.depth = depth
        self.segments = segments
        # meta data
        # need active array 3d - 64xSizexDepth
        self.active = np.zeros((size,64,depth), dtype=np.bool_)
        # need predictive array 3d - 64xSize x Depth
        self.predictive = np.zeros((size,64,depth), dtype=np.bool_)
        # predictive SDR (for estmating)
        self.predSDR = SDR(size)
        # permanence tuples both ways
        # active to predictive(segment,x,y,z,permanence)
        # prdeictive(segment) from active Segments (segment, x,y,z, permanence)
        # 128 segments with 128 dendrites (permanence values) for each segment
        self.cells = [[[Cell(self.segments) for k in range(self.depth)] for j in range(64)] for i in range(self.size)]

        # for each cell, create segments & dendrites(permanence) to random other cells
        for i in range(self.size):
            print("TM: creating row: ",i)
            for j in range(64):
                for k in range(self.depth):
                    # pick a segment
                    #print(i,j,k)
                    for s in range(self.segments): # segment
                        for a in range(100): # 40*4=160  2% od 16k cells (16*64*8)
                            x = int(random.uniform(0,size))
                            y = int(random.uniform(0,64))
                            z = int(random.uniform(0,depth))
                            perm = int(random.uniform(0,256))
                            # permanence to other cells
                            self.cells[i][j][k].addSynapse(s, x, y, z, perm)
                            # going back the other direction
                            self.cells[x][y][z].addFeed(s, i, j, k, perm)
        # firing columns will have the permanence connection to possible predictive cells (both directions - 1 cell checks all that it is connected to to see if it should be in predictive state)


#    def predict(self,inputSDR,pred):

    def feedForward(self,inputSDR,pred):
        # set the inputs
        for i in range(inputSDR.size):
            for j in range(64):
                if inputSDR.get(i,j):
                    # input is true
                    # check if any are predictive
                    found = False
                    for d in range(self.depth):
                        if self.cells[i][j][d].isPredictive():
                            found = True
                            # set all the predictive ones true or just one?
                            self.cells[i][j][d].setActive()
                            self.cells[i][j][d].adjSynapses(inputSDR,1)
                    # none predictive, set them all
                    if not found:
                        for d in range(self.depth):
                            self.cells[i][j][d].setActive()
                            self.cells[i][j][d].adjSynapses(inputSDR,1)
                else:
                    # input is false
                    for d in range(self.depth):
                        self.cells[i][j][d].clearActive()
                        if self.cells[i][j][d].isPredictive():
                            self.cells[i][j][d].adjSynapses(inputSDR,-1)

        for i in range(inputSDR.size):
            for j in range(64):
                for d in range(self.depth):
                    self.cells[i][j][d].resetSegmentCounts()
        
        # create the prediction values (which synapses fired) 
        maxSegCount = 0
        for i in range(inputSDR.size):
            for j in range(64):
                for d in range(self.depth):
                    # if active, push count to predictives
                    if self.cells[i][j][d].isActive():
                        # these are all the synapses that are listening to this cell
                        for syn in self.cells[i][j][d].getFeeds():
                            s,x,y,z,perm = syn.getSynapse()
                            if (perm >= 128): # threshold=32
                                segCount = self.cells[x][y][z].incrementSegmentCounts(s)
                                maxSegCount = max(maxSegCount, segCount)
        # check which cells are now predictive
        print("maxSegCount=",maxSegCount)
        for i in range(inputSDR.size):
            for j in range(64):
                for d in range(self.depth):
                    self.cells[i][j][d].checkPredictive(countTrigger=(maxSegCount*0.7))
                    #self.cells[i][j][d].checkPredictive(countTrigger=(8))

        # return the predicted value of pred

        # create the predicted state matrix
        # train - adjust the permanence weights
        # increment weights on correctly predicted cells
        # decrement weights on predicted cells that didn't win

    def pr(self):
        for i in range(self.size):
            st = ""
            for j in range(64):
                c = 0
                for k in range(self.depth):
                    if self.cells[i][j][k].isActive():
                        c += 1
                if c == 0:
                    st += "."
                else:
                    st += str(c)
            print st

    def prPred(self):
        for i in range(self.size):
            st = ""
            for j in range(64):
                c = 0
                for k in range(self.depth):
                    if self.cells[i][j][k].isPredictive():
                        c += 1
                if c == 0:
                    st += "."
                else:
                    st += str(c)
            print st



if __name__ == "__main__":
    # run test
    test = TemporalMemory(16)
    sdr = SDR(16)
    sdr.randomlyInitialize(0.2)
    sdr.pr()
    test.feedForward(sdr,"Action")
    print
    test.pr()
    print
    test.prPred()
