import Bound
import Bounds
import LowerBounds
import UpperBounds
Bound.Bound.zero = Bound.Bound(path=[],ds=[0,0])

def union_at(theTable:list, theBounds:Bounds, at_i: int, at_j: int):
    for bs in theBounds.getBounds():
        theTable[at_i][at_j].union(bs)

k = 2
G = [ [ 2, 2, 1, 0, 0 ],
      [ 2, 2, 2, 1, 1 ],
      [ 1, 2, 2, 2, 1 ],
      [ 0, 1, 2, 2, 2 ],
      [ 0, 1, 1, 2, 2 ] ]

n = len(G)

UBs = [[UpperBounds.UpperBounds() for _ in range(n) ] for _ in range(n)]
LBs = [[LowerBounds.LowerBounds() for _ in range(n) ] for _ in range(n)]

# FW initialization
for i in range(n):
    for j in range(i, n):

        if G[i][j] != 0:
            b_array = [0 for _ in range(k)]
            b_array[G[i][j] - 1] = 1
            UBs[i][j].union(Bound.Bound(path=[i, j], ds=b_array))
            # print(bd.Bound(ds=b_array))
        UBs[j][i] = UBs[i][j]

        b_array = [0 for _ in range(k)]
        if G[i][j] < k:
            b_array[G[i][j]] = 1
        b_curr = Bound.Bound(path=[i, j], ds=b_array)
        LBs[i][j].union(b_curr)
        LBs[j][i] = LBs[i][j]

# FW recursion
# Flags: all flags work concatenating the walks of bounds.
# notice
# write bounds as a,b and their walks as <u_1,...,u_p> and <v_1,...,v_q>
# when a+b and suppose u_p=v_1, then the concatenation is <u_1,...,v_p=v_1,..v_q>: no flags needed
#
# when a-b, then u_1<=v_1<v_q<=v_q
# -working_with_diagonal -> suppose u_1=v_1 and u_p=v_q (i.e. dist(u_1, u_1) and the walk is a cycle),
# 	then the overlap check need to ignore the two ends;
# -concat_back -->   suppose u_p=v_q, then the path is <u_1,...,u_p=v_q,...v_1>,
# 	then the overlap check need to ignore u_p;
# -concat_front -->  suppose u_1=v_1, then the path is <v_q,...,v_1=u_1,...,u_p>,
# 	then the overlap check need to ignore u_1.
#
# -flip --> notice when subtracting, path of b need to be flipped anyway
#
#
#
for k in range(n):
    for i in range(n):
        for j in range(i, n):
            if i == j:
                Bound.Bound.working_with_diagonal = True
            if i < k < j:
                ub_union = UBs[i][k] + UBs[k][j]
                union_at(theTable= UBs, theBounds= ub_union, at_i= i, at_j= j)

                lb_union = LBs[i][k] + LBs[k][j]
                union_at(theTable= LBs, theBounds= lb_union, at_i = i, at_j= j)

            elif j <= k:
                Bound.Bound.flip = True
                Bound.Bound.concat_back = True
                ub_union = UBs[i][k] - LBs[k][j]
                union_at(theTable= UBs, theBounds = ub_union, at_i=i, at_j= j)
                lb_union = LBs[i][k] - UBs[k][j]
                union_at(theTable= LBs, theBounds= lb_union, at_i=i, at_j=j)
                Bound.Bound.concat_back = False
                Bound.Bound.flip = False


            elif k<= i :
                Bound.Bound.flip = True
                Bound.Bound.concat_front = True
                ub_union = UBs[k][j] - LBs[i][k]
                union_at(theTable= UBs, theBounds= ub_union, at_i=i, at_j=j)
                lb_union = LBs[k][j] - UBs[i][k]
                union_at(theTable= LBs, theBounds= lb_union, at_i=i, at_j=j)
                Bound.Bound.concat_front = False
                Bound.Bound.flip = False

            if i == j:
                Bound.Bound.working_with_diagonal = False

    print("==========iter ", k,"============")
    for i in range(n):
        for j in range(i, n):
            print(UBs[i][j], "\t", end='')
        print("")
    print("\n")
    for i in range(n):
        for j in range(i, n):
            print(LBs[i][j], "\t", end='')
        print("")