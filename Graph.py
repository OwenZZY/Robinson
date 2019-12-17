import numpy as np

class graph:
    def __init__(self, V:list, D:list):
        self.AdjMat = np.zeros((len(V), len(V)))
        self.__V = V[:]
        # self.__E = E
        self.__n = len(V)
        # self.__m = len(E)
        self.levelGraph = []            # levelGraph = [G_(1), G_(2), ..., G_(k)]
        self.D_list = D[:]              # D = [d_1> d_2> d_3> ... >d_k]
        self.R = []
        self.R_p = []
        if len(D)>0:
            self.computeAdjacency(D)

    def computeAdjacency(self, D):
        if D==[] and self.D_list ==[]: return
        self.D_list = D
        self.R = np.zeros((self.__n,len(D)))
        self.R_p = np.zeros((self.__n,len(D)))
        A = self.AdjMat
        for i in range(len(D)):
            self.levelGraph.append(self.__computeAdjWithSingleValue(i))
            A[:] = A + self.levelGraph[i]
        self.AdjMat = A

    def __computeAdjWithSingleValue(self, j):
        """
        :param j: index of distance list
        :return: matrix represents the adjacency matrix given by distance d
        """
        V = self.__V
        n = self.__n
        D = self.D_list
        mat = np.zeros((n,n))
        for mat_row in range(n):
            i = 0
            for i in range(max(mat_row-1,0), n):
                if abs(V[mat_row]-V[i])<= D[j]:
                    mat[mat_row][i] = 1
                    mat[i][mat_row] = 1
                else:
                     i = i-1
                     break
            self.R[mat_row][j] = i
            self.R_p[mat_row][j] = i-mat_row
        return mat

    def r(self, i: int, j: int):
        """
        define function as r_j(i) as the right most entry on row i, with entry value j
        :param i: row number
        :param j: entry value
        :return:
        """
        return self.R[i][j]

    def r_p(self, row: int, val: int):
        """
        :param row: i
        :param val: j
        :return:
        """
        return self.R_p[row][val]