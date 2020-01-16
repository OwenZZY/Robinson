import numpy as np
import D_Polyns as dp
import entry as Entry


class Robinson:

    def __init__(self, n, A, D=1):
        """
        :param n: the size of the matrix,
                        if n is non-zero, then initialize the Robinson by 0
                        if n is zero, initialize the Robinson according to the upper triangle of A
        :param A: the desired Robinson matrix
        :param D:
        """
        self.levelMat = []
        self.__k: int
        self.__k = D
        # self.reachability_i = []
        self.Away = []
        self.WithIn = []
        self.iteration = 0
        self.__R = []  # R[i] is the reachability of the ith iteration, R[i] has shape (__n, __k) where __n is the size of the matrix, __k is the number of d's and in the order of  d[d_1, ..., d_k]
        self.__Rp = []
        if n == 0:  # set Robinson
            self.__letSym(A)
            self.__Robinson = np.array(A)
            self.__n = np.shape(A)[0]
            self.__computeLevelMatrixUsingRobinson()
            # self.__computeRandRp()
        else:
            self.__Robinson = np.diag(np.zeros(n))
            self.__n = n

    def combine_Within_Away(self, within, away):
        if within is None or away is None:
            print("Error: Empty parameter")
            return

        newWithin = [[None for _ in range(self.__n)] for _ in range(self.__n)]
        for i in range(self.__n):
            for j in range(i, self.__n):
                within[i][j]: Entry
                newWithin[i][j] = within[i][j]

    def init_Within_Entry(self):
        """
        Initialized the within table
        :return:
        """
        currWithinIn = [[None for _ in range(self.__n)] for _ in range(self.__n)]
        self.__within_recursive(currWithinIn, 0, self.__n - 1)
        self.WithIn.append(currWithinIn)

    def __within_recursive(self, currWithin: list, i, j):
        # if entry [i, j] is not empty
        # then by dynamic programming: the entry is computed already
        if currWithin[i][j] is not None:
            return
        # Base case: if the i, j adjacent.
        # then it is the shortest edge between each other
        if i == j - 1:
            ent = Entry.entry()
            arr = [0 for _ in range(self.__k)]
            for t in range(self.__k):
                if self.__R[0][i][t] == 0:
                    arr[t - 1] = 1
                    break
                if t == self.__k - 1 and self.__R[0][i][t] != 0:
                    arr[t] = 1
            f = dp.D_polyns(0, arr)
            ent.addPolyn(f)
            currWithin[i][j] = ent
            currWithin[j][i] = ent
            return

        # otherwise, compute recursively
        # for each i, j, by the following diagram
        """
        abcd...zE
                a
                b
                c
                ...
                z
        """
        # and add up all the a's, b's, ..., z's to obtain the best lower bounds
        # see document for intuition
        for k in range(i + 1, j):
            self.__within_recursive(currWithin, i, k)
            self.__within_recursive(currWithin, k, j)
        currWithin[i][j] = Entry.entry()
        self.__when_initial_within_table_entry_dp_IH(currWithin, i, j)
        self.__findDirectEdge(currWithin, i, j)
        currWithin[j][i] = currWithin[i][j]

    def __findDirectEdge(self, currWithin: list, i, j):
        currentEntry: Entry = currWithin[i][j]
        arr = [0] * self.__k
        for t in range(self.__k - 1, -1, -1):
            if self.__R[0][i][t] >= j:
                arr[t] = 1
                f = dp.D_polyns(k=0, array=arr)
                currentEntry.renewListWRTMinMax(f,0)
                break
        return

    def __when_initial_within_table_entry_dp_IH(self, currWithin, i, j):
        """Used only for within_recursive"""
        currentEntry: Entry = currWithin[i][j]
        for k in range(i + 1, j):
            # print("doing ",str(i), str(k), str(j))
            ListA: Entry = currWithin[i][k]
            ListB: Entry = currWithin[k][j]

            for p in range(len(ListA)):
                for q in range(len(ListB)):
                    f: dp.D_polyns = ListA.get(p) + ListB.get(q)
                    currentEntry.renewListWRTMinMax(f,0)

    def checkContradiction(self):
        """
        this method iterates through within and away table, check each entry such that the bounds do not contradicts to
        each other
        :return: return boolean that returns the position of wrong bound (i, j)
                    if the bounds are fine return true
        """
        away = self.Away[self.iteration]
        within = self.WithIn[self.iteration]
        n = self.__n
        for i in range(n):
            for j in range(i+1, n):
                print((i,j))
                Aw: Entry = away[i][j]
                Wi: Entry = within[i][j]
                Check = Aw.allAreLower(Wi)
                if not Check:
                    return (i, j)
        return True

    def init_Away_Entry(self):
        """
         At the end of this function, the program should have
         The Robinson object should consist of
         self.levelMat: all level graphs
         self.__k: the size

         The first layer of
         self.iteration = 0
         self.Away[0]
         self.WithIn[0]
         self.__R [0]
         self.__Rp = [0]
        :return:
        """
        n = self.__n
        Rob = self.__Robinson
        D = self.__k

        tblAway = [[Entry.entry() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                val = Rob[i][j]
                if val < D:
                    ply2 = [0] * D
                    ply2[val] = 1
                    f2 = dp.D_polyns(D, ply2)
                    tblAway[i][j].addPolyn(f2)
                    # tblAway[j][i].append(f2)
                    tblAway[j][i] = tblAway[i][j]

        self.Away.append(tblAway)

        ## the following will initialize the R and Rp matrix
        lM = self.levelMat
        R_iter = np.zeros((self.__n, len(self.levelMat)))
        Rp_iter = np.zeros((self.__n, len(self.levelMat)))

        for L in range(len(lM)):
            for i in range(self.__n):
                for j in range(i, self.__n):
                    if lM[L][i][j] == 0:
                        R_iter[i][L] = j - 1
                        Rp_iter[i][L] = j - 1 - i
                        break
                    elif lM[L][i][j] != 0 and j == self.__n - 1:
                        R_iter[i][L] = j
                        Rp_iter[i][L] = j - i
        self.__R.append(R_iter)
        self.__Rp.append(Rp_iter)

    def updateRandRpOne(self):
        R_iter = np.array(self.__R[len(self.__R) - 1])
        Rp_iter = np.zeros((self.__n, len(self.levelMat)))
        R_c = self.__R[0]  # len(self.__R) - 1]
        Rp_c = self.__Rp[len(self.__Rp) - 1]
        for t in range(self.__k):  # for each distance d
            for i in range(self.__n):  # for each row
                R_iter[i][t] = R_c[int(R_iter[i][t])][t]
        return R_iter, Rp_iter

    def updateRandRp(self):
        same = False
        while not same:
            same = True
            # target = np.ones(self.__k)*(self.__n-1)
            tup = list(self.updateRandRpOne())
            # tup = list(tup)
            front = self.__R[len(self.__R) - 1]

            for i in range(self.__n):
                for t in range(self.__k):
                    # print(str(target[t]),str(tup[0][i][t]) )
                    if front[i][t] != tup[0][i][t]:
                        same = False
                        break
                if not same:
                    break
            if not same:
                self.__R.append(tup[0])
                self.__Rp.append(tup[1])
            # print(same)

    def init_both(self):
        self.init_Away_Entry()
        self.updateRandRp()
        self.init_Within_Entry()
        self.iteration = 0

    def update_Bounds(self):
        """
        This function will append another within and Away table to the end of self.Within and self.Away
        :return:
        """
        oldUpperBound = self.WithIn[self.iteration]
        oldLowerBound = self.Away[self.iteration]
        ## To compute new within table, use within away new within
        ## To compute new away table, use away within new away

        self.computeNewTable(oldUpperBound, oldLowerBound, self.WithIn, minmax= 0) # compute new within
        self.computeNewTable(oldLowerBound, oldUpperBound, self.Away, minmax = 1) # compute new away
        self.iteration += 1

    def computeNewTable(self, Front, Back, Append, minmax: int):
        n = self.__n
        newTable = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                self.computeNewEntryAt(i, j, Front, Back, newTable, minmax=minmax)
                pass
        Append.append(newTable)

    def computeNewEntryAt(self, indexi, indexj, oldFront, oldBack, newFront, minmax: int):
        """
        :param indexi:
        :param indexj:
        :param oldFront:
        :param oldBack:
        :param newFront: Entry
        :param minmax: 0=> minimal, 1=> maximal
        :return:
        """
        newEntry = oldFront[indexi][indexj].copy()

        for k in range(0, indexi):
            newE = oldFront[indexj][k] - oldBack[indexi][k]
            # if indexi == 3 and indexj == 4:
            #     print("Within"+ "("+str(indexj)+","+str(k)+") - Away"+ "("+str(indexi)+","+str(k)+")" )

            newEntry.appendEntryWRTMinMax(newE, minmax)

        for k in range(indexj + 1, self.__n):
            # if indexi == 3 and indexj == 4:
            #     print("Within"+ "("+str( indexi)+","+str(k)+") - Away"+ "("+str(indexj)+","+str(k)+")" )
            newE = oldFront[indexi][k] - oldBack[indexj][k]

            newEntry.appendEntryWRTMinMax(newE, minmax)

        newFront[indexi][indexj] = newEntry
        newFront[indexj][indexi] = newEntry

    def __str__(self):
        ret = ""
        away = self.Away
        within = self.WithIn
        ret += "Away:\n"
        for i in range(self.__n):
            for j in range(self.__n):
                ret += str(away[0][i][j]) + "\t\t\t"
            ret += "\n"
        # ret += "Away 2:\n"
        # for i in range(self.__n):
        #     for j in range(self.__n):
        #         ret += str(away[1][i][j]) + "\t\t\t"
        #     ret += "\n"
        ret += "\nWithin 0:\n"
        for i in range(self.__n):
            for j in range(self.__n):
                if within[0][i][j] is not None:
                    ret += "(" + str(i) + ", " + str(j) + "): " + str(within[0][i][j]) + "\t"
                else:
                    ret += "[]" + "\t\t\t\t"
            ret += "\n"
        # ret += "\nWithin 1:\n"
        # for i in range(self.__n):
        #     for j in range(self.__n):
        #         if within[1][i][j] is not None:
        #             ret += "(" + str(i) + ", " + str(j) + "): " + str(within[1][i][j]) + "\t"
        #         else:
        #             ret += "[]" + "\t\t\t\t"
        #     ret += "\n"
        return ret

    def __letSym(self, A):
        n = len(A)
        for i in range(n):
            for j in range(i + 1, n):
                A[j][i] = A[i][j]

    def setMat(self, A: list):
        if len(A) != len(A[0]):
            print("Matrix is not square")
            return
        self.__n = len(A)
        for i in range(self.__n):
            for j in range(i, self.__n):
                if A[i][j] != A[j][i]:
                    print("Matrix is not symmetric")
                    return
        self.__Robinson = np.array(A)
        self.__computeLevelMatrixUsingRobinson()

    def __computeLevelMatrixUsingRobinson(self):
        NonZero = 0
        A = self.__Robinson
        for i in range(self.__n):
            for j in range(i, self.__n):
                if A[i][j] != 0:
                    NonZero = NonZero + 1
        tempAM = np.array(self.__Robinson)
        while NonZero > 0:
            level_t = np.diag(np.ones(self.__n))
            for i in range(self.__n):
                for j in range(i, self.__n):
                    if tempAM[i][j] > 0:
                        level_t[i][j] = 1
                        level_t[j][i] = 1
                        tempAM[i][j] = tempAM[i][j] - 1
                        tempAM[j][i] = tempAM[j][i] - 1
                        if tempAM[i][j] == 0:
                            NonZero = NonZero - 1
            self.levelMat.append(np.array(level_t))


"""Not needed"""
"""

def reachableMatrix(self):
    reachableMat = []
    for A in self.levelMat:
        reachableMat.append(self.__reachProduct(A, A))
    return reachableMat


def __reachProduct(self, A, B):
    obt = np.matmul(A, B)
    for i in range(self.__n):
        for j in range(self.__n):
            if obt[i][j] == 0:
                obt[i][j] = 0
            else:
                obt[i][j] = 1
    return obt
    

"""
