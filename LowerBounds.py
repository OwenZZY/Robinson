import UpperBounds as ubds
import Bounds as bds
import Bound as bd

class LowerBounds(bds.Bounds):
    def whatami(self):
        return "LowerBounds"
    def __init__(self, toCpy=None):
        super().__init__(toCpy=toCpy)

    def union(self, elt):
        if elt is None:
            return False
        removeIndex = []
        bounds = self.bounds
        toAdd = True

        for i in range(len(bounds)):
            if bounds[i] <= elt:
                removeIndex.append(i)
            if elt <= bounds[i]:
                toAdd = False
                break
        if not toAdd:
            return
        removeIndex.reverse()
        for ind in removeIndex:
            bounds.pop(ind)
        bounds.append(elt)
        return toAdd

    def __sub__(self, U_Bds:ubds):
        if not isinstance(U_Bds, ubds.UpperBounds):
            raise Exception("Given para expect UpperBounds")
        ret = LowerBounds()
        L = self.getBounds()
        U = U_Bds.getBounds()
        for l in L:
            for u in U:
                ret.union(l - u)
        return ret

    def __add__(self, otherB):
        ret = LowerBounds()
        this = self.bounds
        other = otherB.getBounds()
        for b1 in this:
            for b2 in other:
                ret.union(b1+b2)
        return ret
