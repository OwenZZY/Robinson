import numpy as np

class D_polyns:

    def __init__(self, k=0, array=None):
        """
        k will give a list of size k, say coeff[k]
        :param k: integer represents the size of the D_list
        """
        if array is None:
            self.coeff = np.zeros(k)
            self.__k = k
        else:
            self.__k = len(array)
            self.coeff = np.array(array)
            self.singleton = self.__isSingleton()

    def __isSingleton(self):
        # return the index of the singleton if it is one
        # otherwise return -1
        C = self.coeff
        e = -1
        for i in range(len(C)):
            if C[i] != 0:
                if e == -1:
                    e = i
                else:
                    return -1
        return e



    def canReplace(self, other):
        """
        This method suppose to provide info about the replacability
        0: they are incomparable i.e. it should be added to the entry
        1: this is a better bound than other
        -1: this is a worse bound than other, we should discard it immediately
        :param other: D_polyns
        :return:
        """
        if not isinstance(other, self.__class__):
            print("Need a ", str(self.__class__))
            return False
        if len(other) != self.__k:
            print("Length of ", str(self.__class__), "is different, incomparable")
            return False

        if self==other:
            return -1
        if self<other:
            return 1
        if other<self:
            return -1
        return 0

    def __lt__(self, other):
        """
        Strictly less than implies all elements are less or equal to the other
        And there are at least one element that is strickly less than the poly
        :param other:
        :return:
        """
        Other = other.coeff
        This = self.coeff
        cummulation = 0
        nStrict = False
        for i in range(self.__k):
            cummulation += This[i] - Other[i]
            if cummulation > 0:
                nStrict = True
                break
        if not nStrict:
            return 1
        """
        if self.__basicCmp(other)!= 0:
            return NotImplemented
        s = self.coeff
        o = other.coeff
        flag = False
        for i in range(len(self)):
            if s[i] > o[i]:
                return False
            if s[i]< o[i]:
                flag = True
        return flag and True
        """

    def reset(self, k=0, array=None):
        if array is None:
            self.coeff = np.zeros(k)
            self.__k = k
        else:
            self.__k = len(array)
            self.coeff = np.array(array)

    def addAt(self, pos: int, val: int=1):
        self.coeff[pos] += val
        return True

    def setAt(self, pos: int, val: int=0):
        self.coeff[pos] = val
        return True

    def __len__(self):
        return self.__k

    def __basicCmp(self, other):
        """
        function return non-negative integer,
        0 implies the comparison is fine, else not implemented
        :param other:
        :return:
        """
        if not isinstance(other, D_polyns):
            print("Require ", str(self.__class__))
            return 1
        if len(self) != len (other):
            print("Require equal length")
            return 2
        return 0

    def __le__(self, other):
        if self.__basicCmp(other) != 0:
            return NotImplemented
        s = self.coeff
        o = other.coeff
        for i in range(len(self)):
            if s[i] > o[i]:
                return False
        return True



    def __ge__(self, other):
        if self.__basicCmp(other) != 0:
            return NotImplemented
        s = self.coeff
        o = other.coeff
        for i in range(len(self)):
            if s[i] < o[i]:
                return False
        return True

    def __gt__(self, other):
        if self.__basicCmp(other) != 0:
            return NotImplemented
        s = self.coeff
        o = other.coeff
        flag = False
        for i in range(len(self)):
            if s[i] < o[i]:
                return False
            if s[i]> o[i]:
                flag = True
        return flag and True

    def __eq__(self, other):
        if self.__basicCmp(other) != 0:
            return NotImplemented
        s = self.coeff
        o = other.coeff
        for i in range(len(self)):
            if s[i] != o[i]:
                return False
        return True

    def __ne__(self, other):
        if self == other:
            return False
        return True

    def __str__(self):
        ret = ""
        n = len(self.coeff)
        L = True
        #if self.singleton != -1:
        #    ret += "("+str(self.singleton)+")"
        for i in range(n):
            c = self.coeff[i]
            if  c == 0:
                continue
            if not L:
                ret += " + "
            L = False
            if c == 1:
                ret += "d_"+str(i+1)
            else:
                ret += str(self.coeff[i]) + "d_" + str(i + 1)

        if ret=="": return str(0)
        return ret

    def __add__(self, other):
        arr = [0 for _ in range(self.__k)]
        for i in range(self.__k):
            arr[i] = self.coeff[i]+ other.coeff[i]
        f = D_polyns(k=0,array=arr)
        return f

    def __sub__(self, other):
        arr = [0 for _ in range(self.__k)]
        for i in range(self.__k):
            arr[i] = self.coeff[i] - other.coeff[i]
        f = D_polyns(array=arr)
        return f