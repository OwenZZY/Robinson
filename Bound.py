"""
Define bound
"""
import numpy as np


def linearly_combine_for(T):
    T_ = []
    for i in range(len(T)):
        for j in range(i, len(T)):
            T_.append(T[i]+T[j])
    for t_ in T_:
        T.append(t_)


class Bound:

    def linearly_combine(self):
        linearly_combine_for(self.positive_bound)
        linearly_combine_for(self.negative_bound)

    def try_throw_in(self, elt, set: list):
        if set == self.positive_bound:
            if self.zero<= self:
                return
        else:
            if self <= self.zero:
                return
        for bs in set:
            bs: Bound
            if bs.divides(elt):
                return
        set.append(elt)

    def add_to_positive_bound(self):
        if self.zero <= self:
            return
        add = True
        for b in self.positive_bound:
            if b.divides(self):
                add = False
                break
        if add:
            self.positive_bound.append(self)
            self.try_throw_in(self.zero - self, self.negative_bound)


    def add_to_negative_bound(self):
        if self <= self.zero:
            return
        add = True
        for b in self.negative_bound:
            if b.divides(self):
                add = False
                break
        if add:
            self.negative_bound.append(self)
            self.try_throw_in(self.zero - self, self.positive_bound)

    positive_bound = [] # if upper bound + positive bound, then it is not a better upper bound.
    negative_bound = [] # if lower bound + negative bound, then it is not a better lower bound.
    zero = 0

    def is_a_negative_bound(self):
        N = self.negative_bound
        for n in N:
            if n.divides(self) or self<=n:
                return True
        return False

    def is_a_positive_bound(self):
        P = self.positive_bound
        for p in P:  # p:bd.Bound
            if p.divides(self) or p<=self:
                return True
        return False

    def get_positive_bound(self):
        return self.positive_bound

    def divides(self, other): # A|B, so B%A == 0 and B/A = r
        A=self.d
        B=other.get_array()
        # r: ratio, m: divisibility
        # rp:previous r, rs: pre'' s
        pm = None
        i = 0
        while True:

            if A[i]!= 0:
                r = B[i]/A[i]
                m = B[i]%A[i]
                if pm is None:
                    pr = r
                    pm = m

                if pm != m:
                    return False
                if pr != r:
                    return False

            else:
                if B[i]!= 0:
                    return False
            i += 1
            if i == self.k:
                break
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

    def clean_pos_neg_bound(self):
        self.positive_bound = []
        self.negative_bound = []