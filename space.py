class hRegion:
    # create 3D world with given dimension and #faces each
    """ Creates a node in decomposition at given offset.
    If fixedDim != None, this is a surface.  scale is 'diameter' (half side of cube)
    """
    def __init__(self, center=[0,0,0], scale=1, fixedDim=[], parent=None):
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

if __name__ == '__main__':
    tmp = hRegion()
    tmp.subDivide(codim=1)
    tmp1=tmp.subSp[0].subDivide(codim=0)
    vars(tmp1)
