import Bounds as bds
import LowerBounds as lbds

class UpperBounds(bds.Bounds):
    def whatami(self):
        return "UpperBounds"
    def __init__(self, toCpy=None):
        super().__init__(toCpy=toCpy)

    def union(self, elt):
        """
        add another element to bounds
        :param elt:
        :return:
        """
        removeIndex = []
        bounds = self.bounds
        toAdd = True
        # put index of e's\in bounds s.t. elt < e in a removing list to remove
        for i in range(len(bounds)):
            if elt <= bounds[i]:
                removeIndex.append(i)
            if bounds[i] <= elt:
                toAdd = False
        if not toAdd:
            return
        removeIndex.reverse() #delete from the end, it does not destroy the structure
        for ind in removeIndex:
            bounds.pop(ind)
        bounds.append(elt)


    def __sub__(self, L_Bds):
        """
        minus bound with respect as a set of upper bounds
        :param L_Bds:
        :return:
        """
        if not isinstance(L_Bds, lbds.LowerBounds):
            raise Exception("Given para expect LowerBounds")
        ret = UpperBounds()
        U = self.bounds
        L = L_Bds.getBounds()
        for u in U:
            for l in L:
                ret.union(u-l)
        return ret


    def __add__(self, otherB):
        ret = UpperBounds()
        this = self.bounds
        other = otherB.getBounds()
        for b1 in this:
            for b2 in other:
                ret.union(b1+b2)
        return ret