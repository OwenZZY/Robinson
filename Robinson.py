import Table as tbl
import UpperBounds as ubds
import LowerBounds as lbds
import Bound as bd

def print_pn_bd():
    print("-----poss below-----")
    for b in bd.Bound.positive_bound:
        print(str(b) + ",")
    print("-----negs below-----")
    for b in bd.Bound.negative_bound:
        print(str(b) + ",")
    print("--------------------")

class Robinson:

    def __init__(self, G, k):
        self.G = G
        self.n = len(G)
        self.alpha = 0
        self.k = k
        self.L = []
        self.U = []
        self.U.append(self.__constructInitialUpperBoundsTable())
        self.L.append(self.__constructInitialLowerBoundsTable())

        print("-----Initial Upper-----")
        print(self.U[0])
        print("-----Initial Lower-----")
        print(self.L[0])
        print("-----po/ne bounds-----")
        print_pn_bd()


    def find_embedding(self):
        contradiction_at = (-1,-1)
        n = self.n
        while (((self.alpha-1)**2) <= n) and (contradiction_at == (-1,-1)):
            U_alpha = self.U[self.alpha]
            L_alpha = self.L[self.alpha]

            U_alpha_temp = U_alpha + U_alpha
            L_alpha_temp = L_alpha + L_alpha

            U_alpha_1 = U_alpha_temp - L_alpha
            L_alpha_1 = L_alpha_temp - U_alpha
            self.U.append(U_alpha_1)
            self.L.append(L_alpha_1)

            self.alpha += 1
            # print("Tent within\n", U_alpha_temp, "\nTent away\n", L_alpha_temp)
            print("Within table\n", self.U[self.alpha], "\nAway table\n", self.L[self.alpha])
            contradiction_at = self.no_contradiction()
            print("-------iter ", str(self.alpha), " ends-----")
            print_pn_bd()

        if contradiction_at != (-1,-1):
            print("Contradiction at", contradiction_at)
            return False

        print("No contradiction", contradiction_at)
        return True

    def no_contradiction(self)->(int,int):
        L_T:lbds = self.L[self.alpha]
        U_T:ubds = self.U[self.alpha]
        #L = L_T.getTable()
        #U = U_T.getTable()
        n = self.n
        for i in range(n):
            for j in range(i, n):
                if L_T.getAt(i,j).causes_contradiction(
                        U_T.getAt(i,j)):
                    print(str(L_T.getAt(i,j)),  " versus ",U_T.getAt(i,j))
                    return (i,j)
        return -1, -1

    def L_at(self, i):
        return self.L[i]
    def U_at(self, i):
        return self.U[i]

    def __constructInitialUpperBoundsTable(self):
        n, k, G = self.n, self.k, self.G

        T = [[ubds.UpperBounds() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                curr = T[i][j]

                if G[i][j] != 0:
                    b_array = [0 for _ in range(k)]
                    b_array[G[i][j]-1] = 1
                    curr.union(bd.Bound(path=[i,j],ds=b_array))
                    #print(bd.Bound(ds=b_array))
                T[i][j]=curr
        return tbl.Table(withArray=T)

    def __constructInitialLowerBoundsTable(self):
        n, k, G = self.n, self.k, self.G

        T = [[lbds.LowerBounds() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                curr = T[i][j]
                b_array = [0 for _ in range(k)]
                if G[i][j] < k:
                    b_array[G[i][j]] = 1
                b_curr = bd.Bound(path=[i,j], ds=b_array)

                curr.union(b_curr)

                T[i][j] = curr
        return tbl.Table(withArray=T)
