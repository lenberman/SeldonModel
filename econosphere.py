from econosphereBase import * 

now = 0



        #  self.capacity = capacity  # (UseValue,capacity,unit cost)  in agreement class
class Inclusion(edg):
    def __init__(self, *src, target=None, forward=False, end=None, start = now):
        super().__init__(src, target, forward, end, start)

class Meiotic(edg):
    def __init__(self, *src, target=None, forward=True, end=None, start = now):
        super().__init__(src, target, forward, end, start)

class Mitotic(edg):
    def __init__(self, *src, target=None, forward=True, end=None, start = now):
        super().__init__(src, target, forward, end, start)

class Agreement(edg):
    def __init__(self, src, target, forward=True, end=None, start = now):
        super().__init__(src, target, forward, end, start)

    def addPromise(self,uv):...

class bNode(Node):
    @classmethod
    def zygote(cls, name, info=None):
        try:
            return Node.nodes[name]
        except KeyError:
            Node.nodes[name] =  bNode(name, info)
            z = Node.nodes[name]
            z.zygote = True
        return z
        
    def __init__(self, name=None, info=None, event=Event()):
        super().__init__(self, info,event)
        self.zygote = False


class iNode(Node):
    sorts = [ "Zygotic", "Commercial", "Governmental", "Institutional" ]

    @classmethod
    def  iZygote(cls, nd):
        assert(nd.zygote == True)
        assert(False)

    def __init__(self, gov=None, poss=None, event=Event(), info=None, mny=None,name=None):
        super().__init__(self, info, event)
        if poss is None:
            self.possessions = {} #owned cNodes
        else:
            self.possessions = poss
        self.name = name
        self.money = mny


# linked to geometry
class Government(iNode):
    indx = 0
    def  __init__(self, region, laws=None, nm=None): 
        if nm is None:
            nm = "gov" + str(Government.indx)
            Government.indx += 1
        super().__init__(self, laws, name=nm)
        self.region = region
        self.nation = False

    @classmethod
    def getInsitution(cls, participants, name, rules=None):
        external = participants[0].nation
        for gov in participants.items():
            assert(external is gov[1].nation)
        inst = Institution(participants, name)
        return inst
            

    # internal governmental subdivision
    def getSubGov(self, size):
        reg = Region(self.region.locales, size)
        reg = Government(reg)
        edge = reg.addEdge(self, Mitotic, False)
        return reg

## World holds regions and Nations.  Links  geometry to nodes.
class World(Government):
    disputeRS = None
    
    # create world with given dimension and #faces each 
    def __init__(self, extent, dimension=3, faces=6):
        self.dimension = dimension
        self.faces = faces
        self.extent = extent
        self.shape = [ faces ]
        self.states = list()
        size = faces
        for i  in range(dimension-1):
            self.shape.append(extent)
            size *= extent
        self.surface = {}
        for i in range(size):
            rem = i//faces
            coord = list()
            coord. append(i%faces)
            for j in range(dimension-1):
                coord.append(rem%extent)
                rem //= extent
            self.surface[tuple(coord)] = {}

    def getNation(self, size):
        reg = self.getRegion( size)
        gov = Government(reg)
        gov.nation = True
        self.states.append(gov)
        edge = gov.addEdge(self, edgClass=Inclusion, fwd=False)
        return gov

    def __str__(self):
        rv = "Dimension(" + str(self.dimension)  + "), Extent(" + str(self.extent) + ")\n"
        rv += str(self.shape) +"\n" + str(self.surface)
        return rv
        
    def getRegion(self, size):
        assert(size <= len(self.surface))
        return Region(self.surface, size)


class Institution(iNode):
    # Adds institution with govList members
    def __init__(self, govList, nm):
        super().__init__(self, name=nm)
        for member in govList.values():
            member.addEdge(tgt=self, edgClass=Meiotic)


class Commerce(Node):
    def __init__(self, possessor:iNode, factory=True, cInfo=None):
        super().__init__(self, cInfo)
        self.owner = possessor
        self.info = cInfo
    ...

if __name__ == '__main__':    
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.show()
