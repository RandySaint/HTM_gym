# Class for a Cell in the TemporalMemory data structure

import numpy as np
from Synapse import Synapse
from SDR import SDR
import random

class Cell(object):
    def __init__(self,numSegments):
        # links to other cells (x,y,z) with Permanence values : (x,y,z,p)
        self.feeds = [] # list of 'links' to cells - when i'm active, set their predictive
        self.numSegments = numSegments
        self.segCount = np.zeros(numSegments)
        self.segments = [[] for s in range(numSegments)] # List of lists : segment, 'links'
        self.winningSegment = 0
        self.predictive = False
        self.active = False

    def resetSegmentCounts(self):
        self.segCount = [0 for s in range(self.numSegments)]
    
    def incrementSegmentCounts(self, s):
        self.segCount[s] += 1
        return self.segCount[s]

    def addSynapse(self, S, X, Y, Z, P):
        self.segments[S].append(Synapse(X,Y,Z,P,S))

    def addFeed(self, S, X, Y, Z, P):
        self.feeds.append(Synapse(X,Y,Z,P,S))
    
    def getFeeds(self):
        return self.feeds

    def adjSynapses(self, sdr, val): # increment value
        for syn in self.segments[self.winningSegment]: # will winning Segment alwasy be set, or do we need to calculate it?
            # if syn points to an active column
            x, y, z = syn.getXYZ()
            if sdr.get(x,y):
                syn.adjPermanence(val)

    def checkPredictive(self, countTrigger):
        # assumes the callign program has already adjusted Segment Counts
        self.predictive = False
        bestCount = 0
        bestS = 0
        for s in range(self.numSegments):
            if self.segCount[s] >= countTrigger:
                self.predictive = True
                if self.segCount[s] > bestCount:
                    bestCount = self.segCount[s]
                    bestS = s
        self.winningSegment = s
        return bestCount

    def isPredictive(self):
        return self.predictive

    def setActive(self):
        self.active = True

    def clearActive(self):
        self.active = False
    def isActive(self):
        return self.active

    def pr(self):
        print("Segments")
        for i in range(self.numSegments):
            print self.segments[i]
        print("Feeds")
        print self.feeds

if __name__ == "__main__":
    # run test
    test = Cell(8) # 8 segments
    test.addSynapse(0, 1,2,3, 15) # to segment 0, add connection to 1,2,3 with strength 15
    test.addSynapse(0, 4,5,6, 45) # to segment 0, add connection to 4,5,6 with strength 45
    for s in range(8):
        for i in range(3):
            test.addSynapse(s, random.uniform(0,100),random.uniform(0,100),random.uniform(0,100), random.uniform(0,256))
    test.addFeed(0, 4,5,6, 45) # this cell feeds cell 4,5,6 on his segment 0, with strength 45

    print(test.checkPredictive(30))
    print("Active:", test.isActive())
    print("Predictive:", test.isPredictive())
    test.pr()


