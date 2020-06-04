"""
Define bound
"""
import numpy as np

class Bound:
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