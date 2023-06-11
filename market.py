from econosphere import *

""" Simple string language for specify simple sequences of time intervals, relative to the current time.  Linear sequence of offsets: init@period*k 
"""
class TimeSpec:
    @classmethod
    def checkSpec(cls, spec):
        pass
        
    """ Verifies the interval is valid, """
    @classmethod
    def checkInterval(cls, tpl):
        return tpl[0] < tpl[1]


""" Simple string language for specify simple sequences of time intervals, relative to the current time.  Linear sequence of offsets: init@period*k 
"""
class Decode:
    def __init__(self, string:str):
        if string.__class__ == int:
            string=str(string)
        atIndx =string.find("@")
        starIndx = string.find("*")
        if atIndx >= 0:
            if atIndx == 0:
                init = 0
            else:
                init = int(string[0:atIndx])
        else:
            init = 0
            atIndx = 0
        if starIndx < 0:
            period = string[atIndx:]
            repeats = None
        else:
            period = string[atIndx+1:starIndx]
            repeats = string[starIndx+1:]
        self.at = init
        self.repeats = repeats
        self.period = period

    def getLast(self):
        if self.repeats is None:
            return self.at
        if len(self.repeats) == 0 & int(period) != 0:
            return -1
        return int(atIndx) + int(self.period) * int(self.repeats)
        
    def __le__(self, rhs):
        if self.at > rhs.at:
            return False
        elif self.at != rhs.at: 
            return True
        return self.period <= rhs.period
        
    def __gt__(self, rhs):
        return not rhs <= self
        
    def __lt__(self, rhs):
        if self.at > rhs.at:
            return False
        elif self.at != rhs.at: 
            return True
        return int(self.period) <= int(rhs.period)
        
    def __ge__(self, rhs):
        return not rhs < self
        
class Offer:
    oNum = 0
    """itemList is sequence of (cNode, quantity) pairs, trans... When, Where and until may
    each be a single value or lists of the same length as itemList.  offer (T/F) and
    price  indicate whether package is being offered(T) or requested(F) 
    the associated suggested price if any.

    """
    def __init__(self, *, who:iNode, itemList:UseValue, quantity=1,
                 transWhere, transWhen=NOW, offer, price=None, until=None):
        self.what = itemList
        self.quantity = quantity
        self.valid = (Decode(transWhen), Decode(until))
        try:
            assert TimeSpec.checkInterval(self.valid)
        except Exception:
            pdb.set_trace()
        self.where = transWhere
        self.sell = offer
        self.price = price
        self.who = who
        Offer.oNum += 1
        self.oNum = Offer.oNum
        
class Contract:
    def __init__(self, o0:Offer, o1:Offer):
        self.pair = [o0, o1]
        self.acceptedBy = [ False, False]

        """ Register & report acceptance of the contract, i.e. the pair of offers.
               Returns True if both parties have accepted.
        """
    def accept(self, obligee):
        if obligee is None:
            return self.acceptedBy[0] and self.acceptedBy[1]
        if  obligee == self.o1.who:
            self.acceptedBy[0] = True
        elif  obligee == self.o2.who:
            self.acceptedBy[1] = True
        else:
            assert False
        return self.acceptedBy[0] and self.acceptedBy[1]

class Market(Institution):
    def __init__(self, *, money:cNode, govList, openAt=NOW):
        super().__init__(govList=govList, nm=money.name+"Market")
        self.addEdge(tgt=money, edgClass=Mitotic)
        self.openAt=openAt
        self.mny = money
        self.offerList = {}
        self.acceptedOfferList = []
        assert not money is None

        """ Place offer on correct Q and checks for immediate match.  Returns True
        """
    def submit(self, *,offer=None):
        matched = self.match(offer)
        if not matched is None:
            self.acceptedOfferList.append((offer, matched))
            return True
        tList = self.offerList.get(offer.valid[0])
        if tList is None:
            self.offerList[offer.valid[0]] = [offer]
        else:
            tList.append(offer)
        return True

    def match(self, offer):
        pass

    """ Process/respond to current offers
    """
    def tick(self):
        pass

Node.nodeColors[ Market] = "silver"
Node.nodeStyle = { World : "rounded", Government: "wedged", Institution:  "bold",
                    iNode: "dashed", bNode : "dotted", cNode: "diagonals" ,
                   Market: "filled", Node: "black"}
