import Bound as bd
import UpperBounds as ubds
import LowerBounds as lbds

class FW:

    def FW_algo(self):
        n = len(self.graph)
        dist = self.graph
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if (dist[i][k] + dist[k][j]) <= dist[i][j]:
                        dist[i][j] = dist[i][k]+dist[k][j]

    def __init__(self, G, k):
        self.G = G
        self.k = k
        self.positive_bound = []
        self.negative_bound = []
        self.graph = self.__init_graph(G)
        pass

    def __init_graph(self, G):
        n = len(G)
        k = self.k
        ret = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                ret[i][j] = ubds.UpperBounds()
                if G[i][j] != 0:
                    b_array = [0 for _ in range(k)]
                    b_array[G[i][j]-1] = 1
                    ret[i][j].union(bd.Bound(ds=b_array))
        for i in range(n):
            for j in range(i):
                ret[i][j] = lbds.LowerBounds()
                b_array = [0 for _ in range(k)]
                if G[i][j] < k:
                    b_array[G[i][j]] = 1
                b_curr = bd.Bound(ds=b_array)
                ret[i][j].union(b_curr)
        for i in range(n):
            ret[i][i] = ubds.UpperBounds()
            ret[i][i].union(bd.Bound([0 for _ in range(self.k)]))
        return ret

    def __str__(self):
        ret = ""
        n = len(self.graph)
        for i in range(n):
            for j in range(n):
                ret += str(self.graph[i][j])+"\t"
            ret+= "\n"
        return ret