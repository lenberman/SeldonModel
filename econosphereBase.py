#!/usr/bin/python3
""" Provides Base classes for graph and geometry """
import random
import statistics
import math
import sys
import pdb
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.sparse import dok_array

NOW = 0
#import pdb; pdb.set_trace()


class hRegion:
    # create 3D world with given dimension and #faces each
    """ Creates a node in decomposition at given offset.
    If fixedDim != None, this is a surface.  scale is 'diameter' (half side of cube)
    """
    def __init__(self,*, center=[0,0,0], scale=1, fixedDim=[], parent=None, root=None):
        if root is None:
            self.path = []
            self.center = center
            self.scale = scale
            self.fixed = fixedDim
            self.next = 0
            self.faces = {} # faces of hyper-cube
            self.subSpace = {} # sub hyper cubes of same dimension
            self.parent = parent
            if parent is None:
                self.path = ["/"]
            if not parent is None:
                self.parent.addSub(self)
            return
        else:
            assert root.__class__ is hRegion
            self.path = root.path.copy().append("./")
            self.parent = root.parent
            self.center = root.center
            self.scale = root.scale
            self.fixed = root.fixed.copy()
            self.next = 0
            self.faces = {} # faces of hyper-cube
            self.subSpace = {} # sub hyper cubes of same dimension
            #import pdb; pdb.set_trace()#pdb.set_trace()
            self.parent.addSub(self)
            return

    def matches(self,hR):
        return (self.center == hR.center)  and\
             (self.scale == hR.scale) and\
            (self.fixed == hR.fixed)

    def addSub(self, hR): #actually replaces a matching hR
            if len(self.fixed) !=len(hR.fixed):
                assert not hR in self.faces.values()
                hR.path = self.path.copy() + [["-",len(self.faces.keys())]]
                # find & replace matching item in self.faces
                for kyz in self.faces.keys():
                    if hR.matches(self.faces[kyz]): # matches checks center,dim, and scale
                        self.faces[kyz] = hR
                        return
                self.faces[len(self.faces.keys())] = hR
            else:
                assert not hR in self.subSpace.values()
                hR.path = self.path.copy() + [["=",len(self.subSpace.keys())]]
                self.subSpace[len(self.subSpace.keys())] = hR

    """
    chunk(self,codim) returns faces of given codim.
    """
    def chunk(self, codim):
        if self.next.__class__ is hRegion:
            return self.next.chunk(codim)
        if codim==len(self.fixed) and len(self.subSpace) == 0:
            self.subDivide(codim=0)   #divide region
            return self.chunk(codim)
        elif codim>len(self.fixed) and len(self.faces) == 0:
            self.subDivide(codim=1)   # create faces of region
            return self.chunk(codim)
        if len(self.fixed)==1 and self.next < len(self.subSpace)  - 1:
            rv = self.subSpace[self.next]
            self.next += 1
            return rv
        elif len(self.fixed)==0 and self.next < len(self.faces)  - 1:
            rv = self.faces[self.next]
            self.next += 1
            return rv
        if len(self.fixed) != codim:
            self.next = self.faces[self.next].subDivide(codim=0)
        else:
            self.next = self.subSpace[self.next].subDivide(codim=0)
        return self.chunk(codim)
        

            
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
            scale = self.scale
            for coor in range(len(self.center)):
                offset = self.center.copy()
                fd = self.fixed.copy()
                if not coor in fd:
                    fd.append(coor)
                    face = True
                if not coor in self.fixed:
                    offset[coor] = offset[coor] +  self.scale
                #self.faces[2*coor] = hRegion(center=offset, scale=self.scale, fixedDim=fd, parent=self)
                hRegion(center=offset, scale=self.scale, fixedDim=fd, parent=self)
                offset = self.center.copy()
                if not (coor in self.fixed):
                    offset[coor] = offset[coor] - self.scale
                #self.faces[2*coor+1] = hRegion(center=offset,scale=self.scale,fixedDim=fd, parent = self)
                hRegion(center=offset,scale=self.scale,fixedDim=fd, parent = self)
        return self

    
class Event:  # space time chunk starting NOW
    """" time and space """
    events = {}

    @classmethod
    def getChunk(cls, t=NOW, i=None, j=None, k=None):
        try:
            return Event.events[(t, (i,j,k) )]
        except KeyError:
            return  Event(t, i, j, k)

    def __init__(self, t=NOW, i=None, j=None, k=None):
        self.time = t
        self.space = (i,j,k)
        assert Event.events.get((self.time,self.space)) is None
        Event.events[(self.time,self.space)] = (self.time,self.space)

    def __str__(self):
        return "(@" + str(self.time) + "T, loc:" + str(self.space) + ")"


""" Use values may are hierarchical.   """
class UseValue:
    """ Examples include: fear power friendship love medium-of-exchange """
    uvList = {}
    uvId = 0
    """
    Define a new UseValue (or retrieve by name existing uv).  
    If cn is not None, it specifies a set of non-derived UVs
    """
    @classmethod
    def  UV(cls, name, uVector=None):    #list(name) relates this UV to previous
        assert   (name.__class__ is str) or  (name.__class__ is int) 
        obj = cls.uvList.get(name)
        if  obj is None:   # create UseValue
            obj = UseValue(name=name, uVector=uVector)
        return obj

    """ Resets fundamental, i.e. non-derivative use values."""
    @classmethod
    def resetUV(cls, *, uvList):
        cls.uvList = uvList
        uvId = len(UseValue.uvList)

        """ 
        uvs = ( name|uvId , +/-val ) +.  If uvs is None, new UseValue
        """
    def __init__(self, *, name, uVector=None):
        UseValue.uvId += 1
        assert name.__class__ is str
        self.name = name
        self.uvId = UseValue.uvId
        self.uv = uVector
        UseValue.uvList[ name ] = self
        UseValue.uvList[ self.uvId ] = self


    def __str__(self):
        return self.name + ":(uvId=" + str(self.uvId) + "): " + str(self.uv)

#  directed  edges with (multi-dimsensional) capacity and adjustable delay.
class Edge:
    """ 4 different semantic types of edges """
    edgeTypes = {}
    edgeColors = {}
    @classmethod
    def connect(cls, src, tgt):
        return cls(src, tgt)

    def __str__(self):
        return str(vars(self.edge[0])) + "\n\t>>\n" + str(vars(self.edge[1])) + \
            "@(" + str(self.start) + ", " + str(self.end) + ")\n"

    # create edge from (src->tgt || tgt->src)
    def __init__(self, src=None , tgt=None, end=None, start = NOW, label = None):
        self.edge = [src, tgt]
        self.start = start
        self.end = end
        key = -1
        if not Node.mDiGraph is None:
            key=self.getGraphKey()
            if label is None:
                Node.mDiGraph.add_edge(src.name, tgt.name, key=key, cls=self.__class__)
            else:
                Node.mDiGraph.add_edge(src.name, tgt.name, key=key, cls=self.__class__, label=str(label))

    def getGraphKey(self):
        key=-1
        for pairs in Edge.edgeTypes.items():
            key += 1
            if pairs[1] is self.__class__:
                return key
        pdb.set_trace()
        return key + 1

    def reverse(self):
        self.edge = (self.edge[1], self.edge[0])


##Node
class Node:   # # Node in Seldon decomposition
    """ Base class for all nodes """
    indx = 0
    nodes = {}
    nodeColors = {}
    mDiGraph = None
    # create out-edges from self to tgt
    def __rshift__(self, tgt):
        for target in tgt:
            nodeTgt = target[0](target[1])
        return edge

    def __init__(self, name=None, event=None):  # # any Node may have lifetime
        # increment then stor
        Node.indx += 1
        self.name = name
        self.nId = Node.indx
        if self.name is None:
            self.name = "Node_" + str(self.nId)
        self.edges = []
        self.birth = event
        self.geo = None
        self.info= None
        self.power = None
        self.fear = None
        self.addToGraph(Node.mDiGraph)

    def setName(self, nm):
        del Node.nodes[self.name]
        self.name = nm
        Node.nodes[self.name] = self

    def addToGraph(self,g):
        if not g  is None:
            g.add_node(self.name, cls=self.__class__)
        assert Node.nodes.get(self.name) is None
        Node.nodes[self.name] = self
        
    """ retrieves """
    @classmethod
    def getNode(cls, name):
        nd = Node.nodes.get(name)
        if not nd is None:
            assert isinstance(nd, cls)
            return nd
        return None


    def addEdge(self, *,tgt, edgClass, start=None, end=None, label=None):
        for edg in self.edges: # only one inclusion edge with a given src.
            if edg.__class__ is Edge.edgeTypes["Inclusion"] and edgClass is Edge.edgeTypes["Inclusion"]:
                oldSrc = edg.edge[0]
                oldTgt = edg.edge[1]
                try:
                    oldSrc.edges.remove(edg)
                    oldTgt.edges.remove(edg)
                    Node.mDiGraph.remove_edge(oldSrc.name, oldTgt.name, key=edg.getGraphKey())
                except ValueError:
                    pdb.set_trace()
                    assert False
        tmp = edgClass(src=self, target=tgt,label=label)
        assert not self is tgt
        self.edges.append(tmp)
        if not tgt is None:
            tgt.edges.append(tmp)
        return tmp

    # returns list (possibly empty) of self-edges possibly to other, of given class and direction from self
    def getEdges(self, *, edgClass, out=None, other=None):
        rv = []
        for edge in self.edges:
            if not edge.__class__ is edgClass:
                continue
            if ((out==True)  and self is edge.edge[0]) and ((other is None) or (other is edge.edge[1])):
                rv.append(edge)
                continue
            if ((out==False)  and self is edge.edge[1]) and ((other is None) or (other is edge.edge[0])):
                rv.append(edge)
                continue
        return rv

    """
    If stopNodeClass
    """
    def ancestors(self, *, edgClass, stopNodeClass, forward):
        rv = []
        val = [self]
        for e in self.edges:
            if e.__class__ is edgClass:
                other = None
                if e.edge[0] is self and forward:
                    other = e.edge[1]
                elif not forward and e.edge[1] is self:
                    other = e.edge[0]
                if other is None: #edgClass correct, direction incorrect
                    continue
            else:
                continue  #wrong edgClass.
            # correct edgClass and other != None
            val.append(other)
            if other.__class__ is stopNodeClass or stopNodeClass is None:
                rv += [val]
                val = [self]
                continue
            else:  #
                val += other.ancestors(edgClass=edgClass, stopNodeClass=stopNodeClass, forward=forward)
                rv += [val]
                val = self
                break
        return rv


    def __str__(self):
        rv = str(vars(self)) + str(self.birth)
        return rv

    def where(self, when=NOW):...

    def step(self, until=NOW+1):
        ...


Node.nodes = {}
Node.indx = 0

if __name__ == '__main__':
    nd = Node("test", None)
    nd1 = Node("test1", None)
    edge = nd >> nd1
    pprint(str(edge))
    pprint(str(nd))
