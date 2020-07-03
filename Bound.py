"""
Define bound
"""
from __future__ import annotations

import numpy as np


def _linearly_combine_for(T):
    T_ = []
    for i in range(len(T)):
        for j in range(i, len(T)):
            sum_ = T[i]+T[j]
            if sum_ is None:
                continue
            T_.append(sum_)
    for t_ in T_:
        T.append(t_)

def linearly_combine():
    Bound.concat_freely = True
    _linearly_combine_for(Bound.positive_bound)
    _linearly_combine_for(Bound.negative_bound)
    Bound.concat_freely = False

def try_throw_in(elt, target_set: list):
    neg_elt = Bound.zero - elt

    if target_set == Bound.positive_bound:
        if Bound.zero <= elt:
            return
    else:
        if elt <= Bound.zero:
            return
    for bs in target_set:
        if bs.divides(neg_elt):
            return
    target_set.append(neg_elt)

def cat_paths(path1:list, path2:list):
    """
    The input expect an path [u,...,v] with u<v
    (so it starts from left, ends somewhere right)
    So the end of path1 should matches end of path 2
    :param path1: list
    :param path2: list
    :return:
    """
    # print(path1, path2)
    if Bound.flip_first:
        path1.reverse()
    if Bound.flip_second:
        path2.reverse()
    if path1[len(path1)-1] != path2[0]:
        raise Exception("Mismatch path endpoints", str(path1), str(path2))
    return path1+path2[1:]

class Bound:

    positive_bound = []  # if upper bound + positive bound, then it is not a better upper bound.
    negative_bound = []  # if lower bound + negative bound, then it is not a better lower bound.
    zero = None
    flip_first = False
    flip_second = False
    concat_freely = False

    def add_to_positive_bound(self):
        if Bound.zero <= self:
            return
        add = True
        for b in Bound.positive_bound:
            if b.divides(self):
                add = False
                break
        if add:
            cpy = self.cpy()
            Bound.positive_bound.append(cpy)
            try_throw_in(cpy, Bound.negative_bound)


    def add_to_negative_bound(self):
        if self <= Bound.zero:
            return
        add = True
        for b in Bound.negative_bound:
            if b.divides(self):
                add = False
                break
        if add:
            cpy = self.cpy()
            Bound.negative_bound.append(cpy)
            try_throw_in(cpy, Bound.positive_bound)

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

    def divides(self, other):
        """
        the operation is A|B,
        so B%A == 0 and B/A = r
        :param other:
        :return:
        """
        A=self.d
        B=other.get_array()
        previous_remainder = None
        previous_ratio = None
        k = len(A)
        for t in range(k):
            if A[t]!= 0:
                ratio = B[t]/A[t]
                remainder = B[t]%A[t]
                if previous_remainder is None:
                    previous_remainder = remainder
                    previous_ratio = ratio

                if previous_remainder != remainder:
                    return False
                if previous_ratio != ratio:
                    return False
            else:
                if B[t]!= 0:
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

    def __init__(self, path:list ,ds=None, dim=0, toCpy=None):
        self.k = dim
        self.path = path
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
        return Bound(path= self.path,ds=self.get_array())

    def dim(self):
        return self.k

    def get_array(self):
        return self.d

    def __add__(self, other):
        if self.__add_sub_error(other) is True:
            return None

        path1 = self.path
        path2 = other.path
        arr1 = self.d
        arr2 = other.d

        ret = arr1 + arr2
        if not Bound.concat_freely:
            return Bound(cat_paths(path1[:], path2[:]),
                         ds=ret)
        else:
            return Bound(path=[],ds=ret)

    def __sub__(self, other:Bound):
        if self.__add_sub_error(other) is True:
            return None
        if self == Bound.zero:
            return Bound(path=other.path[:], ds= -other.d)

        arr1 = self.d
        arr2 = other.d
        ret = arr1 - arr2
        if Bound.flip_second:
            return Bound(cat_paths(self.path[:],other.path[:]), ds=ret)
        elif Bound.flip_first:
            return Bound(cat_paths(other.path[:], self.path[:]) ,ds= ret)


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
