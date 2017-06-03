class Synapse:
    def __init__(self, x, y, z, perm, seg=-1):
        self.x = x
        self.y = y
        self.z = z
        self.perm = perm # permanence strength 0-255
        self.seg = seg # segment this synapse belongs to

    def __str__(self):
        return "[%i](%i,%i,%i) = %i" % (self.seg, self.x, self.y, self.z, self.perm)
    def __repr__(self):
        if self.seg >= 0:
            return "[%i](%i,%i,%i)=%i" % (self.seg, self.x, self.y, self.z, self.perm)
        else:
            return "(%i,%i,%i)=%i" % (self.x, self.y, self.z, self.perm)

    def getPermanence(self):
        return self.perm

    def adjPermanence(self, val):
        self.perm = min(255,max(0,self.perm+val)) # limit to 0-255

    def isActive(self, threshold):
        return self.perm > threshold

    def getXYZ(self):
        return self.x,self.y,self.z

    def getSXYZ(self):
        return self.seg,self.x,self.y,self.z

    def getSynapse(self):
        return self.seg,self.x,self.y,self.z,self.perm

if __name__=="__main__":
    syn = Synapse(1,2,3,255)
    print(syn)
    print(syn.isActive(50))
    den = Synapse(4,5,6,15,2)
    print(den)
    print(den.isActive(50))
    mylist = [[] for i in range(3)]
    mylist[0].append(Synapse(1,2,3,14,0))
    mylist[0].append(Synapse(4,5,6,55,0))
    mylist[1].append(Synapse(8,9,10,11,1))
    for myl in mylist:
        print(myl)
