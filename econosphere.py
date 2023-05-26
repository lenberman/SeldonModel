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
        super().__init__(name, event)
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
        super().__init__(name, event)
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

class hRegion(iNode):
    # create 3D world with given dimension and #faces each
    """ Creates a node in decomposition at given offset.
    If fixedDim != None, this is a surface.  scale is 'diameter' (half side of cube)
    """
    def __init__(self, center=[0,0,0], scale=1, fixedDim=[], parent=None):
        super().__init__(self)
        self.center = center
        self.scale = scale
        self.fixed = fixedDim
        self.faces = [] # faces of hyper-cube
        self.subSpace = [] # sub hyper cubes of same dimension
        self.parent = parent
        if not parent is None:
            if len(self.fixed) !=len(parent.fixed):
                parent.faces.append(self)
            else:
                parent.subSp.append(self)
        return self

    """ Subdivides into cubes(codim==0) or faces of cube(codim==1)
              Needs checking for 2D or 4D 
    """
    def subDivide(self, codim = 1):
        SIGN = [ (1, 1, 1), (-1, 1, 1), (1, -1, 1), (-1, -1, 1), (1, 1, -1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1)]
        if codim == 0:
            scale = self.scale*.5
            for sigNdx in range(2**(len(self.center)-len(self.fixed))):
                offset = []
                ith = 0 # ith counts non-face dimensions, thus remaining in faces listed in self.fixed
                for coor in range(len(self.center)): # loop over changing coordinates
                    if not coor in self.fixed:
                        offset.append(self.center[coor]+scale*SIGN[sigNdx][ith])
                        ith += 1
                for  coor in self.fixed: 
                    offset.insert(coor,self.center[coor])
                hRegion(center=offset, scale=self.scale*.5, fixedDim=self.fixed, parent=self)
        elif codim == 1:
            for coor in range(len(self.center)):
                offset = self.center.copy()
                fd = self.fixed.copy()
                if not coor in fd:
                    fd.append(coor)
                    face = True
                if not coor in self.fixed:
                    offset[coor] = offset[coor] +  self.scale
                hRegion(center=offset, scale=self.scale, fixedDim=fd, parent=self)
                offset = self.center.copy()
                if not (coor in self.fixed):
                    offset[coor] = offset[coor] - self.scale
                hRegion(center=offset,scale=self.scale,fixedDim=fd, parent = self)
        return self



# linked to geometry
class Government(hRegion):
    indx = 0
    governmentFunctions = { "citizen" : None , "corp" : None , "tax" : None, "MoneySupply" : None,
                            "Market" : None }

    """  # makes  iNodes in tgtList subordinate to self, returns tgtList """
    def __lshift__(self, tgtList):
        nList = list()
        for commerce in tgtList:
            assert commerce.__class__ is iNode
            self.naturalize(commerce)
        return tgtList

    """ Creates named subordinate Government nodes from names in tgtList.
    """
    def __rshift__(self, tgtList):
        nList = list()
        for nam in tgtList:
            z=self.getSubGov(nm=nam,siz=1)
            z.addEdge(self, edgClass=Inclusion, fwd=False)
            nList.append(z)
        return nList

    def  __init__(self, laws=None, nm=None):
        super().__init__(self)
        if nm is None:
            nm = "g_" + str(Government.indx)
            Government.indx += 1
        self.prop4ExternalViolence = None
        self.prop4InternalViolence = None
        self.moneySupply = None
        self.nation = False

    """ Insures """
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

    """Get's list of citizens of gov't """
    def getCitizenList(self):
        czlf = governmentFunctions["citizen"]
        

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
        nList = []
        for nat in tgtList:
            nList.append(self.getNation(nat[0], nat[1]))
        return nList

    # returns list of zygotes with World inclusion.
    def __rshift__(self, tgtList):
        nList = []
        for nat in tgtList:
            z=bNode.zygote(nat)
            z.addEdge(self, edgClass=Inclusion, fwd=False)
            nList.append(z)
        return nList

    # create world with given dimension and #faces each
    def __init__(self, extent, nm1="Earth", dimension=3):
        super().__init__(self)
        Node.setName(self, nm1)

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


""" Institutions may be the target of inclusion nodes and provide their own decision
  mechanismsintermediate, court systems..  """
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
