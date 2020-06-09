import UpperBounds as ubds
import Bounds as bds

class LowerBounds(bds.Bounds):
    def whatami(self):
        return "LowerBounds"
    def __init__(self, toCpy=None):
        super().__init__(toCpy=toCpy)

    def union(self, elt):
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
                if u.is_a_positive_bound():
                    continue
                ret.union(l - u)
        return ret

    def __add__(self, otherB):
        ret = LowerBounds()
        this = self.bounds
        other = otherB.getBounds()
        for b1 in this:
            if b1.is_a_positive_bound():
                continue
            for b2 in other:
                if b2.is_a_positive_bound():
                    continue
                ret.union(b1+b2)
        return ret
