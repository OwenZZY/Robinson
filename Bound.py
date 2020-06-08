"""
Define bound
"""
import numpy as np

class Bound:

    def add_to_positive_bound(self):
        add = True
        for b in self.positive_bound:
            if b.divides(self):
                add = False
                break
        if add:
            self.positive_bound.append(self)
        pass

    def add_to_negative_bound(self):
        add = True
        for b in self.negative_bound:
            if b.divides(self):
                add = False
                break
        if add:
            self.negative_bound.append(self)

    positive_bound = [] # if upper bound + positive bound, then it is not a better upper bound.
    negative_bound = [] # if lower bound + negative bound, then it is not a better lower bound.

    def is_a_negative_bound(self):
        N = self.negative_bound
        for n in N:
            if n.divides(self):
                return True
        return False

    def is_a_positive_bound(self):
        P = self.positive_bound
        for p in P:  # p:bd.Bound
            if p.divides(self):
                return True
        return False

    def get_positive_bound(self):
        return self.positive_bound

    def divides(self, other): # A|B, so B%A == 0 and B/A = r
        A=self.d
        B=other.get_array()
        ratio = B/A
        sign = B%A
        r,s = ratio[0], sign[0]
        for i in range(self.k):
            if r != ratio[i] or s != sign[0]:
                return False
        return True

    def __le__(self, other):
        if self == other:
            return True
        sa, sb = 0, 0
        k = self.k
        for i in range(k):
            sa += self.at(i)
            sb += other.at(i)
            if sa > sb:
                return False
        return True

    def __ge__(self, other):
        if self == other:
            return True
        sa, sb = 0, 0
        k = self.k
        for i in range(k):
            sa += self.at(i)
            sb += other.at(i)
            if sa < sb:
                return False
        return True

    def __eq__(self, other):
         for i in range(self.k):
             if self.at(i) != other.at(i):
                 return False
         return True

    def at(self, index):
        return self.d[index]

    def __init__(self, ds=None, dim=0, toCpy=None):
        self.k = dim
        if dim != 0:
            self.d = np.zeros(self.k)
        elif ds is not None:
            self.d = np.array(ds)
            self.k = len(self.d)
        elif toCpy is not None:
            if not isinstance(toCpy, Bound):
                raise Exception("Not a Bound Var")
            self.d = np.array(toCpy.get_array())
            self.k = toCpy.dim()

    def cpy(self):
        return Bound(self.get_array())

    def dim(self):
        return self.k

    def get_array(self):
        return self.d

    def __add__(self, other):
        if self.__add_sub_error(other) is True:
            return None
        ret = np.zeros(self.k)
        arr1 = self.d
        arr2 = other.d

        ret = arr1 + arr2
        return Bound(ds=ret)

    def __sub__(self, other):
        if self.__add_sub_error(other) is True:
            return None
        ret = np.zeros(self.k)
        arr1 = self.d
        arr2 = other.d

        ret = arr1 - arr2

        return Bound(ds=ret)

    def __add_sub_error(self, other):
        if not isinstance(other, type(self)):
            print("Type error")
            return True
        if self.k != other.dim():
            print("Length error")
            return True
        return False

    def __str__(self):
        return str(self.d)