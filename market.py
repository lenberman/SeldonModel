from econosphere import *

""" Simple string language for specify simple sequences of time intervals, relative to the current time.  Examples: 
"""
class TimeSpec:
    @classmethod
    def checkSpec(cls, spec):
        pass
        
    @classmethod
    def checkInterval(cls, tpl):
        if tpl[0].__class__ is int and tpl[0].__class__ is int:
            return tpl[0] < tpl[1]
        return False

        
class Offer:
    oNum = 0
    """itemList is sequence of (cNode, quantity) pairs, trans... When, Where and until may
    each be a single value or lists of the same length as itemList.  offer (T/F) and
    price  indicate whether package is being offered(T) or requested(F) 
    the associated suggested price if any.

    """
    def __init__(self, *, who:iNode, itemList:UseValue, quantity=1, transWhere, transWhen=NOW,
                 offer, price=None, until=None):
        self.what = itemList
        self.quantity = quantity
        self.valid = (transWhen, until)
        assert TimeSpec.checkInterval(self.valid)
        self.where = transWhere
        self.sell = offer
        self.price = price
        self.who = who
        Offer.oNum += 1
        self.oNum = Offer.oNum
        

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
