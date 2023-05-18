from  econosphereBase import *
from functools import reduce

#  self.capacity = capacity  # (UseValue,capacity,unit cost)  in agreement class
class Inclusion(Edge):
    def __init__(self, src, target=None, forward=False, end=None, start = NOW):
        super().__init__(src, target, forward, end, start)

class Meiotic(Edge):
    def __init__(self, src, target=None, forward=True, end=None, start = NOW):
        super().__init__(src, target, forward, end, start)

class Mitotic(Edge):
    def __init__(self, src, target=None, forward=True, end=None, start = NOW):
        super().__init__(src, target, forward, end, start)

class Agreement(Edge):
    def __init__(self, src, target=None, forward=True, end=None, start = NOW):
        super().__init__(src, target, forward, end, start)

    def addPromise(self,uv):
        ...

edgeTypes = { "Inclusion" : Inclusion ,
              "Meiotic" : Meiotic,
              "Mitotic" : Mitotic,
              "Agreement" : Agreement}
           

class bNode(Node):
    @classmethod
    def zygote(cls, name, info=None):
        try:
            return Node.nodes[name]
        except KeyError:
            Node.nodes[name] =  bNode(name, info,Event)
            z = Node.nodes[name]
            z.zygote = True
        return z

    def __init__(self, name, info, event):
        super().__init__(name, info,event)
        self.zygote = False


class iNode(Node):
    sorts = [ "Zygotic", "Commercial", "Governmental", "Institutional" ]

    @classmethod
    def  iZygote(cls, nd):
        for edge in nd.edges:
            if edge.__class__ is Inclusion:
                pair = edge.edge
                if pair[0] is nd:
                    gov = pair[1]
                else:
                    gov = pair[0]
        assert gov.__class__ is World
        try:
            Node.nodes[nd.name]
            name= "i_" + nd.name
            iZ = iNode(gov, name)
        except KeyError:
            name=nd.name
            iZ = iNode(gov, name)
        Node.nodes[name] = iZ
        iZ.addEdge(iZ, edgClass=Inclusion)
        return iZ

    def __init__(self, gov=None, poss=None, event=None, info=None, mny=None,name=None):
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
        super().__init__(self)
        if nm is None:
            nm = "gov" + str(Government.indx)
            Government.indx += 1
        super().__init__(self, laws, name=nm)
        self.region = region
        self.nation = False


    # internal governmental subdivision
    def getSubGov(self, size):
        reg = Region(self.region.locales, size)
        reg = Government(reg)
        edge = reg.addEdge(self, Mitotic, False)
        return reg

## World holds regions and Nations.  Links  geometry to nodes.
class World(Government):
    disputeRS = None
    
    # returns list of nations
    def __lshift__(self, tgtList):
        nList = list()
        for nat in tgtList:
            nList.append(self.getNation(nat[0], nat[1]))
        return nList

    # returns list of zygotes
    def __rshift__(self, tgtList):
        nList = list()
        for nat in tgtList:
            z=bNode.zygote(nat)
            z.addEdge(self, edgClass=Inclusion, fwd=False)
            nList.append(z)
        return nList


    # create world with given dimension and #faces each 
    def __init__(self, extent, dimension=3, faces=6):
        super().__init__(self, laws=None)
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

    def getNation(self, name, size):
        reg = self.getRegion( size)
        gov = Government(reg, nm=name)
        gov.nation = True
        self.states.append(gov)
        edge = gov.addEdge(self, edgClass=Inclusion, fwd=False)
        return gov

    def __str__(self):
        rv = "Dimension(" + str(self.dimension)  + "), Extent(" + str(self.extent) + ")\n"
        rv += str(self.shape) +"\n" + str(self.surface) + "\n" + str(self.states)
        return rv
        
    def getRegion(self, size):
        assert(size <= len(self.surface))
        return Region(self.surface, size)


class Institution(iNode):
    # Adds institution with govList members
    def __init__(self, govList, nm):
        super().__init__(self, name=nm)
        for member in govList:
            member.addEdge(tgt=self, edgClass=Meiotic)
        ub = commonAncestors(govList)[0]
        self.addEdge(tgt=ub,edgClass=Inclusion)

class Commerce(Node):
    def __init__(self, possessor:iNode, factory=True, cInfo=None, useValue=None):
        super().__init__(self, cInfo)
        self.owner = possessor
        self.info = cInfo
        self.uv = useValue

def commonAncestors(nds, edgClass=Inclusion, stopNodeClass=World):
    ancestorList = []
    for nd in nds:
        val = nd.ancestors(edgClass, stopNodeClass=World)
        ancestorList.append((val))
    return reduce(commonTail, ancestorList, nds[0].ancestors(Inclusion,World))
               
def commonTail(x, y):
    res = []
    while len(x)>0 and x[len(x)-1] == y[len(y)-1]:
        res.insert(0,x.pop())
        y.pop()
    return res

if __name__ == '__main__':    
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.show()
