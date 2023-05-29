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

    def __init__(self, name=None, gov=None, poss=None, event=None, info=None, mny=None):
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


# linked to geometry
class Government(iNode):
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
            z=self.getSubGov(nm=nam)
            z.addEdge(self, edgClass=Inclusion, fwd=False)
            nList.append(z)
        return nList

    def  __init__(self, name, laws=None, hR=None):
        super().__init__(name=name)
        self.geo = hR
        self.subs = []
        self.prop4ExternalViolence = None
        self.prop4InternalViolence = None
        self.moneySupply = None
        self.nation = False

    """ retrieves """
    def getGovernment(self, name):
        gov = Government.getNode(name)
        if not gov is None:
            assert isinstance(gov,Government)
            return gov
        gov = Government(name)
        if self.__class__ is World:
            gov.nation = True
        edge = gov.addEdge(self, edgClass=Inclusion, fwd=False)
        return gov

    def geometrize(self, hR, frac):
        self.geo = hR.chunkFace()
        # For each subGov (nodes connected by Mitotic edges) geometrize.
        for gov in self.ancestors(Mitotic, Government):
            gov.geometrize(hR, frac)
        

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
        

    # internal governmental subdivision.  Should add inclusion edge 
    def getSubGov(self, nm=None):
        reg = Government(name=nm)
        edge = reg.addEdge(self, Mitotic, False)
        return reg



    ## World holds regions and Nations.  Links  geometry to nodes.
class World(Government):
    disputeRS = None
    
    # returns list of nations
    def __lshift__(self, tgtList):
        nList = []
        for nat in tgtList:
            gov = self.getGovernment(nat)
            if gov.nation:
                self.nations.append(gov)
            nList.append(gov)
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
    def __init__(self, nm1="Earth"):
        super().__init__(nm1, hR=hRegion())
        self.nations = []
        
        """
        If natlist is [], each self.nation gets 1/len(natlist) of the earth's area. Else, natlist is pairs
      [  [ name|gov(name) , num]+ ]
        """
    def geometrize(self):
        xByNatLen = 1.0/len(self.nations)
        for  gov in self.nations:
            assert  gov.nation
            assert isinstance(gov, Government)
            Government.geometrize(gov, self.geo, xByNatLen)
            

    def __str__(self):
        rv = "Dimension(" + str(self.dimension)  + "), Extent(" + str(self.extent) + ")\n"
        return rv

    def getRegion(self, size):
        ...


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
        super().__init__(cInfo)
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
    tmp = hRegion()
    tmp.subDivide(codim=1)
    tmp1=tmp.faces[0].subDivide(codim=0)
    vars(tmp1)
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    #plt.show()
