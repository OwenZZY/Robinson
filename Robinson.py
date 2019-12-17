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
                newWithin[i][j]= within[i][j]

    def initial_Within_Entry(self):
        currWithinIn = [[None for _ in range(self.__n)]for _ in range(self.__n)]
        self.__within_recursive(currWithinIn, 0, self.__n - 1)
        self.WithIn.append(currWithinIn)

    def __within_recursive(self, currWithin: list, i, j):
        if currWithin[i][j] is not None:
            return

        if i == j-1:
            ent= Entry.entry()
            arr = [0 for _ in range(self.__k)]
            for t in range(self.__k):
                if self.__R[0][i][t] == 0:
                    arr[t-1] = 1
                    break
                if t == self.__k-1 and self.__R[0][i][t] != 0:
                    arr[t] = 1
            f = dp.D_polyns(0, arr)
            ent.append(f)
            currWithin[i][j] = ent
            currWithin[j][i] = ent
            return

        for k in range(i+1,j):
            self.__within_recursive(currWithin, i, k)
            self.__within_recursive(currWithin, k, j)
        currWithin[i][j]=Entry.entry()
        self.__Minimal(currWithin, i, j)
        self.__findDirectEdge(currWithin,i,j)
        currWithin[j][i] = currWithin[i][j]

    def __findDirectEdge(self, currWithin:list, i, j):
        currentEntry: Entry = currWithin[i][j]
        arr = [0]*self.__k
        for t in range(self.__k-1, -1 ,-1):
            if self.__R[0][i][t]>=j:
                arr[t] = 1
                f = dp.D_polyns(k=0,array=arr)
                currentEntry.renewList(f)
                break

        return

    def __Minimal(self, currWithin, i, j):
        currentEntry:Entry = currWithin[i][j]
        for k in range(i+1,j):
            # print("doing ",str(i), str(k), str(j))
            ListA: Entry = currWithin[i][k]
            ListB: Entry = currWithin[k][j]

            for p in range(len(ListA)):
                for q in range(len(ListB)):
                    f:dp.D_polyns = ListA.get(p) + ListB.get(q)
                    currentEntry.renewList(f)



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

    def init_Away(self):
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
        #tblWithin = [[Entry.entry() for _ in range(n)] for _ in range(n)]
        # for i in range(n):
        #     f = [0] * D
        #     f[D - 1] = 1
        #    tblWithin[i][i].add(dp.D_polyns(D, f))
        for i in range(n):
            for j in range(i + 1, n):
                val = Rob[i][j]
                if val < D:
                    ply2 = [0] * D
                    ply2[val] = 1
                    f2 = dp.D_polyns(D, ply2)
                    tblAway[i][j].append(f2)
                    tblAway[j][i].append(f2)
        #         if val > 0:
        #             ply1 = [0] * D
        #             ply1[val - 1] = 1
        #             f = dp.D_polyns(D, ply1)
        #             tblWithin[i][j].add(f)
        #             tblWithin[j][i].add(f)
        # self.WithIn.append(tblWithin)
        self.Away.append(tblAway)


        self.iteration = 0
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


    def computeInitialDistance(self):



        return 0

    def InitWithin(self):

        return 0
    def recurInitWithin(self):

        return 0

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

    def updateRandRpOne(self):
        R_iter = np.array(self.__R[len(self.__R)-1])
        Rp_iter = np.zeros((self.__n, len(self.levelMat)))
        R_c = self.__R[0]#len(self.__R) - 1]
        Rp_c = self.__Rp[len(self.__Rp) - 1]
        for t in range(self.__k):  # for each distance d
            for i in range(self.__n):  # for each row
                R_iter[i][t] = R_c[int(R_iter[i][t])][t]
        return R_iter, Rp_iter

    def updateConstraint(self):

        self.iteration += 1

    def computeNewWithIn(self):
        new = np.zeros((self.__n, self.__n))

        self.Away.append(new)

    def computeNewAway(self):
        new = np.zeros((self.__n, self.__n))

        self.WithIn.append(new)

    def __str__(self):
        ret = ""
        away = self.Away
        within = self.WithIn
        ret += "Away:\n"
        for i in range(self.__n):
            for j in range(self.__n):
                ret += str(away[0][i][j]) + "\t\t\t"
            ret += "\n"
        ret += "\nWithin:\n"
        for i in range(self.__n):
            for j in range(self.__n):
                if within[0][i][j] is not None:
                    ret+="("+ str(i)+", "+str(j)+"): "+str(within[0][i][j])+ "\t"
                else:
                    ret += "[]" + "\t\t\t\t"
            ret += "\n"
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