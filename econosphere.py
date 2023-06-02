from  econosphereBase import *
from functools import reduce



#  self.capacity = capacity  # (UseValue,capacity,unit cost)  in agreement class
class Inclusion(Edge):   # 
    def __init__(self, *, src, target=None, end=None, start = NOW):
        super().__init__(src, target, end, start)

class Meiotic(Edge):
    def __init__(self, src, target=None, end=None, start = NOW):
        super().__init__(src, target, end, start)

class Mitotic(Edge):
    def __init__(self, src, target=None, end=None, start = NOW):
        super().__init__(src, target, end, start)

class Agreement(Edge):
    def __init__(self, src, target=None, end=None, start = NOW):
        super().__init__(src, target, end, start)

    def addPromise(self,uv):
        ...

Edge.edgeTypes = { "Inclusion" : Inclusion ,
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
    def  iZygote(cls, nd, gov=None):
        name = nd.name
        foo = Node.nodes.get(name)
        while not foo is None:
            if foo.__class__ is iNode:
                return foo
            else:
                assert foo.__class__ is bNode
                bFoo = foo
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
        iZ = iNode(name, gov=gov)
        bFoo.addEdge(tgt=iZ, edgClass=Inclusion)          
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
        if not gov is None:
            self.addEdge(tgt=gov,edgClass=Inclusion)

    """ iNode operator: rhsList members must exist.   returns commercial iNode with meiotic edges from rhsList
    """
    def __lshift__(self, rhsList):
        assert rhsList[0].__class__ is self.__class__
        owner = self
        if self.zygote:
            _owner = iNode("_"+self.name,self.gov,info=self.info, mny=self.money,event=self.birth)
            owner.addEdge(_owner, edgClass=Meiotic)
        for inode in rhsList:
            if inode.__class__ is "str".__class__:
                inode = Node.nodes[inode]
            inode.addEdge(tgt=_owner, edgClass=Meiotic)
        return

     # returns list of ...
    def __rshift__(self, rhsList):
        print("operatort >> not defined\n")
        for inode in rhsList:
            if inode.__class__ is "str".__class__:
                inode = Node.nodes[inode]
            nList.append(inode)
            self.addEdge(inode, edgClass=Mitotic)
        return nList


# linked to geometry
class Government(iNode):

    governmentFunctions = { "citizen" : None , "corp" : None , "tax" : None, "MoneySupply" : None,
                            "Market" : None }

    """  # makes  iNodes in tgtList have Inclusion edge  to self, returns tgtList with Inclusion adjusted 
    """
    def __lshift__(self, tgtList):
        nList = []
        for commerce in tgtList:
            assert commerce.__class__ is iNode
            self.naturalize(commerce)
        return tgtList

    """ Creates named subordinate Government nodes from names in tgtList.
    """
    def __rshift__(self, tgtList):
        nList = []
        for nam in tgtList:
            assert nam.__class__ is str
            z=self.getSubGov(nm=nam)
            z.addEdge(tgt=self, edgClass=Inclusion)
            nList.append(z)
        return nList

    def  __init__(self, name, laws=None, hR=None):
        super().__init__(name=name)
        self.geo = hR
        self.prop4ExternalViolence = None
        self.prop4InternalViolence = None
        self.moneySupply = None
        self.nation = False

    """ retrieves sub-government under (Inclusion) self  """
    def getGovernment(self, name):
        gov = Government.getNode(name)
        if not gov is None:
            assert isinstance(gov,Government)
            return gov
        gov = Government(name)
        if self.__class__ is World:
            gov.nation = True
        edge = gov.addEdge(tgt=self, edgClass=Inclusion)
        return gov

    def geometrize(self, hR):
        if not self.geo is None:
            assert False
        self.geo = hR.chunk(codim=1)

        # For each subGov (nodes connected by Mitotic edges) geometrize.
        for gov in self.ancestors(edgClass=Mitotic, stopNodeClass=None,forward=True):
            if gov[0]==self:
                cld = gov[1]
            else:
                cld = gov[0]
            cld.geometrize(hR)

        citizenList = []
        for citizen in self.getEdges(edgClass=Inclusion,out=False):
            if citizen.edge[0].__class__ is Government:
                continue
            citizenList.append(citizen.edge[0])
        hR = hRegion(root=self.geo)
        for citizen in citizenList:
            citizen.geo = hR.chunk(codim=1)

            

    """ Insures """
    def naturalize(self, nd):
        assert nd.__class__  is iNode
        edge = nd.getEdges(edgClass=Inclusion, out=True)
        if edge is None:
            edge = nd.addEdge(tgt=self, edgClass=Inclusion)
        elif len(edge) == 1:
            nd.addEdge(tgt=self,edgClass=Inclusion)
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
        edge = self.addEdge(tgt=reg, edgClass=Mitotic)
        return reg



    ## World holds regions and Nations.  Links  geometry to nodes.
class World(Government):
    disputeRS = None
    
    # returns list of nations
    def __lshift__(self, tgtList):
        nList = []
        for nat in tgtList:
            assert nat.__class__ is str
            gov = self.getGovernment(nat)
            nList.append(gov)
        return nList

    # returns list of zygotes with Inclusion target World.
    def __rshift__(self, tgtList):
        nList = []
        for nat in tgtList:
            assert nat.__class__ is str
            z=bNode.zygote(nat)
            z.addEdge(tgt=self, edgClass=Inclusion)
            nList.append(z)
        return nList


    # create world 
    def __init__(self,*, g=None, nm1="Earth"):
        super().__init__(nm1, hR=hRegion())
        Node.diGraph = g
        
        """
        If natlist is [], each self.nation gets 1/len(natlist) of the earth's area. Else, natlist is pairs
      [  [ name|gov(name) , num]+ ]
        """
    def geometrize(self):
        for  gov in self.nations():
            assert  gov.nation
            assert isinstance(gov, Government)
            Government.geometrize(gov, self.geo)
            
    def nations(self):
        nationList = self.getEdges(edgClass=Inclusion, out=False)
        val = list(map(lambda obj: obj.edge[0],filter(lambda obj: obj.edge[0].__class__ is Government, nationList)))
        return val

    def notNations(self):
        nationList = self.getEdges(edgClass=Inclusion, out=False)
        val = list(map(lambda obj: obj.edge[0],filter(lambda obj: not obj.edge[0].__class__ is Government, nationList)))
        return val

    def __str__(self):
        return "World"

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
        val = nd.ancestors(edgClass=edgClass, stopNodeClass=World, forward=True)
        ancestorList.append(val[0])
    ca = reduce(commonTail, ancestorList)
    return ca

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
    print(vars(tmp1))
    plt.plot([1, 3, 2, 4])
    plt.ylabel('some numbers')
    plt.show()
