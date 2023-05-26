class hRegion:
    # create world with given dimension and #faces each
    """ Creates a node in decomposition at given offset.
    If faces != 0 decompose face.
    """
    def __init__(self, center=[0,0,0], codim=1, scale=1, fixedDim=None):
        self.center = center
        self.scale = scale
        self.fixed = []
        self.codim = codim
        self.subSp = []
        if not fixedDim is None:
            self.fixed = fixedDim

            
    def subDivide(self, codim = 1):
        if codim == 0:
            for indx in range(2**len(self.center)):
                offset = []
                for dim in range(len(self.center)):
                    if not dim in self.fixed: 
                        offset.append(self.center[dim]+.5*self.scale*(-1)**(indx//2**dim))
                    else:
                        offset.append(self.center[dim])
                self.subSp.append(hRegion(center=offset, scale=self.scale*.5, codim=0, fixedDim=self.fixed))
        elif codim == 1:
            for indx in range(len(self.center)):
                offset = self.center.copy()
                fd = self.fixed.copy()
                fd.append(indx)
                if not indx in self.fixed:
                    offset[indx] = offset[indx] +  self.scale
                self.subSp.append(hRegion(center=offset, codim=0, scale=self.scale, fixedDim=fd).subDivide(codim=0))
                offset = self.center.copy()
                if not indx in self.fixed:
                    offset[indx] = offset[indx] - self.scale
                self.subSp.append(hRegion(center=offset, codim=0,scale=self.scale,fixedDim=fd).subDivide(codim=0))
        return self

if __name__ == '__main__':
    tmp = hRegion(codim=0)
    tmp.subDivide(codim=1)
    tmp1=tmp.subSp[0].subDivide(codim=0)
    vars(tmp1)
