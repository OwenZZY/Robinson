import Bound
import LowerBounds
import UpperBounds


k = 2
G = [ [ 2, 2, 1, 0, 0 ],
      [ 2, 2, 2, 1, 1 ],
      [ 1, 2, 2, 2, 1 ],
      [ 0, 1, 2, 2, 2 ],
      [ 0, 1, 1, 2, 2 ] ]

n = len(G)

UBs = [[UpperBounds.UpperBounds() for _ in range(n) ] for _ in range(n)]
LBs = [[LowerBounds.LowerBounds() for _ in range(n) ] for _ in range(n)]

for i in range(n):
    for j in range(i, n):
        curr = UBs[i][j]

        if G[i][j] != 0:
            b_array = [0 for _ in range(k)]
            b_array[G[i][j] - 1] = 1
            curr.union(Bound.Bound(path=[i, j], ds=b_array))
            # print(bd.Bound(ds=b_array))
        UBs[i][j] = curr