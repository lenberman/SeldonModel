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

Edge. edgeTypes = { "Inclusion" : Inclusion ,
              "Meiotic" : Meiotic,
              "Mitotic" : Mitotic,
              "Agreement" : Agreement}

class bNode(Node):
    @classmethod
    def zygote(cls, name, info=None):
        try:
            return Node.nodes[name]
        except KeyError:
            bNode(name, info,Event)
            z = Node.nodes[name]
            z.zygote = True
        return z

    def __init__(self, name, info, event):
        super().__init__(name, info,event)
        self.zygote = False


class iNode(Node):
    sorts = [ "Zygotic", "Commercial", "Governmental", "Institutional" ]

    @classmethod  # nd must exist and be connected.
    def  iZygote(cls, nd):
        name = nd.name
        foo = Node.nodes.get(name)
        while not foo is None:
            if foo.__class__ is iNode:
                return foo
            else:
                assert foo.__class__ is bNode
                name= "i_" + name
            foo = Node.nodes.get(name)
        for edge in nd.edges:
            if edge.__class__ is Inclusion:
                pair = edge.edge
                if pair[0] is nd:
                    gov = pair[1]
                else:
                    gov = pair[0]
                break
        assert issubclass(gov.__class__, Government)
        iZ = iNode(name, gov)
        iZ.addEdge(gov, edgClass=Inclusion)
        iZ.zygote = True
        return iZ

    def __init__(self, name, gov=None, poss=None, event=None, info=None, mny=None):
        super().__init__(name, info, event)
        if poss is None:
            self.possessions = {} #owned cNodes
        else:
            self.possessions = poss
        self.money = mny
        self.zygote = False
        self.gov = gov

    # rhsList members must exist.   returns commercial iNode
    def __lshift__(self, rhsList):
        owner = self
        if self.zygote:
            _owner = iNode("_"+self.name,self.gov,info=self.info, mny=self.money,event=self.birth)
            owner.addEdge(_owner, edgClass=Meiotic) 
        for inode in rhsList:
            if inode.__class__ is "str".__class__:
                inode = Node.nodes[inode]
            inode.addEdge(_owner, edgClass=Meiotic)
        return 

     # returns list of ...
    def __rshift__(self, rhsList):
        nList = list()
        for inode in rhsList:
            if inode.__class__ is "str".__class__:
                inode = Node.nodes[inode]
            nList.append(inode)
            inode.addEdge(self, edgClass=Mitotic, fwd=False)
        return nList

# linked to geometry
class Government(iNode):
    indx = 0

    # naturalizes iNodes in tgtList and returns tgtList
    def __lshift__(self, tgtList):
        nList = list()
        for commerce in tgtList:
            assert commerce.__class__ is iNode
            self.naturalize(commerce)
        return tgtList

    # subdivides this with new Government nodes with names given in tgtList.
    # Returns new Government nodes
    def __rshift__(self, tgtList):
        nList = list()
        for nam in tgtList:
            z=self.getSubGov(nm=nam,siz=1)
            z.addEdge(self, edgClass=Inclusion, fwd=False)
            nList.append(z)
        return nList

    def  __init__(self, region=1, laws=None, nm=None):
        super().__init__(nm, laws)
        if nm is None:
            nm = "g_" + str(Government.indx)
            Government.indx += 1
        self.region = region
        self.nation = False

    def naturalize(self, nd):
        assert nd.__class__  is iNode
        edge = nd.getEdges(edgClass=Inclusion)
        if edge is None:
            edge = nd.addEdge(self, Inclusion)
        elif len(edge) == 1:
            edge = edge[0]
            assert edge.edge[0] == nd
            edge.edge[1] = self
        else:
            assert len(edge) == 0
        nd.gov = self
        return edge

    # internal governmental subdivision
    def getSubGov(self, siz=1, nm=None):
        reg = Region(self.region.locales, siz)
        reg = Government(region=reg, nm=nm)
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

    # returns list of zygotes with World inclusion.
    def __rshift__(self, tgtList):
        nList = list()
        for nat in tgtList:
            z=bNode.zygote(nat)
            z.addEdge(self, edgClass=Inclusion, fwd=False)
            nList.append(z)
        return nList

    # create world with given dimension and #faces each
    def __init__(self, extent, nm1="Earth", dimension=3, faces=6):
        super().__init__(self, nm=nm1, laws=None)
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

    def getNation(self, name, size=None):
        if size is None:
            gov = Node.nodes.get(name)
            if not gov is None:
                return gov
        reg = self.getRegion(size)
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
        assert size <= len(self.surface)
        return Region(self.surface, size)


class Institution(iNode):
    # Adds institution with govList members
    def __init__(self, govList, nm):
        super().__init__(nm)
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
