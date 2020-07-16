import Bounds as bds
import Bound as bd
import UpperBounds as ubds
import LowerBounds as lbds


class Table:

    # n is the size of the table, toCpy is another Table to copy
    def __init__(self, n=1,  withArray=None, toCpy=None):
        if withArray is not None and toCpy is not None:
            raise Exception("withArray and toCpy cannot be both not None")

        self.upper_table = False
        if withArray is not None:
            if not isinstance(withArray, list):
                raise Exception("withArray variable expects list, "+type(withArray)+" given." )
            self.n = len(withArray)
            self.table = [[None for _ in range(self.n)] for _ in range(self.n)]

            if isinstance(withArray[0][0], ubds.UpperBounds):
                self.upper_table = True

            for i in range(self.n):
                for j in range(i, self.n):
                    if not (isinstance(withArray[i][j], ubds.UpperBounds) or isinstance(withArray[i][j], lbds.LowerBounds)):
                        raise Exception("Bounds is expected in "+
                                        "withArray at ("
                                        + str(i) +"," + str(j) +"), "
                                        + str(type(withArray)) + " is given."   )

                    self.table[i][j] = withArray[i][j]
                    self.table[j][i] = self.table[i][j]
            return

        if toCpy is not None:
            #if not isinstance(toCpy, type(self)):
            #    raise Exception("toCpy is a "+ str(type(self)) + " Var, "
            #                    + str(type(self))+ " expected.")
            self.n = len(toCpy)
            self.table = [[None for _ in range(self.n)] for _ in range(self.n)]
            if isinstance(toCpy.getAt(0,0), ubds.UpperBounds):
                self.upper_table = True
            c_n = toCpy.n
            for i in range(c_n):
                for j in range(i, c_n):
                    entry = toCpy.getAt(i, j)
                    self.table[i][j] = entry.cpy(type(entry))
                    self.table[j][i] = self.table[i][j]
            return

        self.n = n
        self.table = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i,n):
                self.table[j][i] = self.table[i][j]

    def __len__(self):
        return len(self.table)

    def __str__(self):
        ret = ""
        n = self.n
        T = self
        max_ = 0
        for i in range(n):
            for j in range(n):
                max_ = max(max_, len(T.getAt(i, j)))
        for i in range(n):
            for j in range(i, n):
                a_size = max_ - len(T.getAt(i, j))
                ret +=  ("(" + str(i) + "," + str(j) + "): "
                         + str(T.getAt(i, j)))+"\t"+("\t" * int(a_size/3))
            ret += '\n'

        return ret

    def getTable(self):
        return self.table

    def getAt(self, i, j):
        # return a Bounds object
        return self.table[i][j]

    def addEltAt(self, i, j, elt):
        return self.table[i][j].union(elt)

    def joinBoundsAt(self, i, j, bounds):
        B = bounds.getBounds()
        ret_bd = []
        for b in B:
            if self.addEltAt(i,j, b):
                ret_bd.append(b)
        return ret_bd

    def setAt(self, i, j, bounds):
        self.table[i][j] = bounds

    def __add__(self, otherT):
        """No flag need to be checked"""
        T1, T2 = self.table, otherT.getTable()
        if not isinstance(T1[0][0], type(T2[0][0])):
            raise Exception("Table addition expect same Bounds Type, "
                            + T1[0][0].whatami() + " and "+  T2[0][0].whatami() + " given." )

        retT = Table(toCpy=self)
        for i in range(self.n):
            for j in range(i+1, self.n):
                for k in range(i+1, j):
                    entry = T1[i][k] + T2[k][j]
                    retT.joinBoundsAt(i, j, entry)

        return retT

    def __sub__(self, otherT):
        T1, T2 = self.table, otherT.getTable()
        if isinstance(T1[0][0], type(T2[0][0])):
            raise Exception("Table subtraction expect different Bounds Type, "
                            + T1[0][0].whatami() + " and " + T2[0][0].whatami + " given")

        retT = Table(toCpy=self)
        bd.Bound.flip = True

        for i in range(self.n):
            for j in range(i, self.n):
                if i == j: bd.Bound.working_with_diagonal = True

                bd.Bound.concat_front = True
                for k in range(0, i):
                    entry = T1[k][j] - T2[k][i]
                    ret_bd = retT.joinBoundsAt(i,j, entry)
                bd.Bound.concat_front = False

                bd.Bound.concat_back = True
                for k in range(j+1, self.n):
                    entry = T1[i][k] - T2[j][k]
                    ret_bd = retT.joinBoundsAt(i,j,entry)
                bd.Bound.concat_back = False

                if i == j: bd.Bound.working_with_diagonal = False
        bd.Bound.flip = False
        return retT

    def TypeTable(self):
        ret = ""
        n = self.n
        T = self.table
        for i in range(n):
            for j in range(n):
                ret += (T[i][j].whatami() + "\t")
            ret += "\n"
        return ret