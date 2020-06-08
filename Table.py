import Bounds as bds
import Bound as bd
import UpperBounds as ubds
import LowerBounds as lbds


def add_set_to_negative_bd(set:list):
    for b in set:
        b.add_to_negative_bound()


def add_set_to_positive_bd(set:list):
    for b in set:
        b.add_to_positive_bound()


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
            c_n = toCpy.n
            for i in range(c_n):
                for j in range(c_n):
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
        a_size = 0
        for i in range(n):
            for j in range(n):
                a_size = max_ - len(T.getAt(i, j))
                ret +=  ("(" + str(i) + "," + str(j) + "): " + str(T.getAt(i, j)))+"\t"+("\t" * int(a_size/3))
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
        T1 = self.table
        T2 = otherT.getTable()
        if not isinstance(T1[0][0], type(T2[0][0])):
            raise Exception("Table addition expect same Bounds Type, "
                            + T1[0][0].whatami() + " and "+  T2[0][0].whatami() + " given." )

        retT = Table(toCpy=self)
        for i in range(self.n):
            for j in range(i, self.n):
                for k in range(i, j):
                    entry = T1[i][k] + T2[k][j]
                    # print("("+ str(i)+ ","+str(j)+"): "
                    #       +str( T1[i][k] )+"+"+ str(T2[k][j]))
                    retT.joinBoundsAt(i, j, entry)

        return retT

    def __sub__(self, otherT):
        T1 = self.table
        T2 = otherT.getTable()
        if isinstance(T1[0][0], type(T2[0][0])):
            raise Exception("Table subtraction expect different Bounds Type, "
                            + T1[0][0].whatami() + " and " + T2[0][0].whatami + " given")
        n = self.n
        retT = Table(toCpy=self)
        for i in range(n):
            for j in range(i, n):
                for k in range(0, i):
                    entry = T1[k][j] - T2[k][i]
                    # print("("+ str(i)+ ","+str(j)+"): "
                    #       +str(T1[k][j]) + " - "+ str(T1[k][i]))
                    ret_bd = retT.joinBoundsAt(i,j, entry)
                    if i == j:
                        if isinstance(T1[0][0], ubds.UpperBounds):
                            add_set_to_negative_bd(ret_bd)
                        else:
                            add_set_to_positive_bd(ret_bd)

                for k in range(j+1,n):
                    entry = T1[i][k] - T2[j][k]
                    # print("("+ str(i)+ ","+str(j)+"): "
                    #       +str(T1[i][k])+" - "+str(T2[j][k]))
                    ret_bd = retT.joinBoundsAt(i,j,entry)
                    if i == j:
                        if isinstance(T1[0][0], ubds.UpperBounds):
                            add_set_to_negative_bd(ret_bd)
                        else:
                            add_set_to_positive_bd(ret_bd)

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