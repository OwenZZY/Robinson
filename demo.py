import Graph as gp
import D_Polyns as dp
import Robinson as Rm


def main():
    # G = gp.graph([],[])
    A = [[2, 2, 1, 0, 0, 0],
         [2, 2, 2, 1, 1, 1],
         [1, 2, 2, 2, 1, 1],
         [0, 1, 2, 2, 2, 1],
         [0, 1, 1, 2, 2, 2],
         [0, 1, 1, 1, 2, 2]]
    # G.setAdjMat(A)
    # Reachable = G.reachableMatrix()
    # for A_i in Reachable:
    #     print(A_i)

    C = Rm.Robinson(0, A=A, D=2)
    #C.init_Away_Entry()

    # C.updateRandRp()
    C.init_both()
    #C.computeNewTable(C.WithIn[0], C.Away[0],C.WithIn, 0)
    #C.computeNewTable(C.Away[0], C.WithIn[0],C.Away, 1)
    #C.computeNewTable(C.WithIn[1], C.Away[1], C.WithIn, 0)
    #C.computeNewTable(C.Away[1], C.WithIn[1], C.Away, 1)
    # C.update_Bounds()
    print("Contradiction point: ", C.checkContradiction())
    #C.init_Within_Entry()
    print(C)
    l = [dp.D_polyns(k=0, array=[0, 0, 0, 0, 5]),
         dp.D_polyns(k=0, array=[1, 1, 1, 1, 1]),
         dp.D_polyns(k=0, array=[0, 0, 0, 0, 4]),
         dp.D_polyns(k=0, array=[1, 2, 3, 4, 5]),
         dp.D_polyns(k=0, array=[1, 0, 3, 4, 5]),
         dp.D_polyns(k=0, array=[0, 2, 3, 4, 5])]
    a = dp.D_polyns(k=0, array=[1, -2])
    b = dp.D_polyns(k=0, array=[0, 1])

    # for i in range(len(l)):
    #     for j in range(len(l)):
    #         print(str(i)+", "+str(j)+": ",str(l[i])+" cmp to "+ str(l[j])+": ", str(l[i].canReplace(l[j])))

    print(a.canReplace(b))



if __name__ == "__main__":
    print("Do")
    main()
