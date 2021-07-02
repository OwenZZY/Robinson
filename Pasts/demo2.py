import scipy

import Bounds as bds
import Bound as bd
import Table as tbl
import UpperBounds as ubds
import LowerBounds as lbds
import Robinson as Rob
import numpy as np
from scipy.optimize import linprog


def embed_with(Pi, d):
    print("Pi=", Pi)
    print("D=", d)
    A = np.zeros((n, n))
    for d_t in d:
        A_i = np.zeros((n, n))
        # print(d_t)
        for u in range(n):
            for v in range(n):
                if abs(Pi[u] - Pi[v]) <= d_t:
                    A_i[u, v] = 1
        print(A_i)
        A += A_i
    return A


# G = [ [ 2, 2, 1, 0, 0, 0 ],
#       [ 2, 2, 2, 1, 1, 1 ],
#       [ 1, 2, 2, 2, 1, 1 ],
#       [ 0, 1, 2, 2, 2, 1 ],
#       [ 0, 1, 1, 2, 2, 2 ],
#       [ 0, 1, 1, 1, 2, 2 ] ]
# R = Rob.Robinson(G,  k = 2)
# R.find_embedding()


k = 2
bd.Bound.zero = bd.Bound(path=[], ds=[0 for _ in range(k)])
# G = [[3, 2, 1, 1, 0, 0, 0],
#      [2, 3, 3, 2, 1, 1, 0],
#      [1, 3, 3, 2, 1, 1, 0],
#      [1, 2, 2, 3, 2, 2, 1],
#      [0, 1, 1, 2, 3, 2, 1],
#      [0, 1, 1, 2, 2, 3, 2],
#      [0, 0, 0, 1, 1, 2, 3 ]]
G = [[2, 2, 1, 0, 0],
     [2, 2, 2, 1, 1],
     [1, 2, 2, 2, 1],
     [0, 1, 2, 2, 2],
     [0, 1, 1, 2, 2]]
# G = [[2,2,1],
#      [2,2,2],
#      [1,2,2]]
n = len(G)

R = Rob.Robinson(G, k=k)
found = R.find_embedding()

if not found:
    print("Not embeddable")
    exit(0)
print("Claim: embeddable")

# exit(0)

print("Linear program")
U = R.U_at(R.alpha)
L = R.L_at(R.alpha)

print(U, "\n", L)

A = []
b = []

print("Constructing Linear Program...\n")

for u in range(n):
    upper_bounds_at_uv: bds.Bounds = U.getAt(u, u)
    lower_bounds_at_uv: bds.Bounds = L.getAt(u, u)
    # x = [0 for i in range(n)]

    #            x[u] += -1
    #            x[v] += 1
    for bound in upper_bounds_at_uv.bounds:
        if bound == bd.Bound.zero:
            continue
        restriction = list(-bound.d)
        if not restriction in A:
            A.append(restriction)
            b.append(0)
        pass

    # x = [0 for i in range(n)]
    # x[u] += 1
    # x[v] += -1
    for bound in lower_bounds_at_uv.bounds:
        if bound == bd.Bound.zero:
            continue
        restriction = list(bound.d)
        if not restriction in A:
            A.append(restriction)
            b.append(-(10e-6))
        pass
    pass

"""
A:
      d1 d2 d3
res1
res2
...

b: b_i <- constant constrain of res1, with <= connects them
(b_i)
"""
print("\nPrinting Linear Program...\n")
dummy = [1 for i in range(k)]
print("A: ", np.array(A))
print("b: ", b)
# np.set_printoptions(precision=1)
# print(np.append(np.array(A),
#                 np.array(b).reshape((len(b),1)),
#                 axis= 1))

res = linprog(dummy,
              A_ub=A,
              b_ub=b,
              bounds=[(1, None) for _ in range(k)])
# print(res)
# np.set_printoptions(precision=5)
print("\nLine 119, print result: \n", np.array(res.x), "\n\n")

A = np.zeros((n, n))
scalar_upperbd = [[[] for _ in range(n)] for _ in range(n)]
scalar_lowerbd = [[[] for _ in range(n)] for _ in range(n)]
U = R.U_at(R.alpha).table
L = R.L_at(R.alpha).table

## [  2.85  23.16  44.96  81.19  87.11 117.94  73.96]
# D = res.x[n:]
d = res.x[:]
print("Threshold vector d=", d)
for u in range(n):
    for v in range(u, n):
        B_uv = U[u][v].bounds
        for b in B_uv:
            scalar = np.dot(b.d, d)
            if not (scalar in scalar_upperbd[u][v]):
                scalar_upperbd[u][v].append(scalar)
        B_uv = L[u][v].bounds
        for b in B_uv:
            scalar = np.dot(b.d, d)
            if not (scalar in scalar_lowerbd[u][v]):
                scalar_lowerbd[u][v].append(np.dot(b.d, d))

# useless, just printing
# for u in range(n):
#     for v in range(n):
#         if v<u:
#             print("[] ",end="\t")
#         else:
#             print(scalar_upperbd[u][v],end="\t")
#     print()
# print()
# for u in range(n):
#     for v in range(n):
#         if v<u:
#             print("[] ",end="\t")
#         else:
#             print(scalar_lowerbd[u][v],end="\t")
#     print()

Wrong = False
for u in range(n):
    for v in range(u, n):
        if max(scalar_lowerbd[u][v]) > min(scalar_upperbd[u][v]):
            print("Contradiction at: (", u, ",", v, "):", max(scalar_lowerbd[u][v]), ",", min(scalar_upperbd[u][v]))
            Wrong = True
print("Contradiction", end="")
if Wrong: exit(0)

Pi = [0 for _ in range(n)]
Pi[0] = 0

for v in range(1, n):
    lb = max([Pi[i] + max(scalar_lowerbd[i][v]) for i in range(v)])
    ub = min([Pi[i] + min(scalar_upperbd[i][v]) for i in range(v)])
    if lb >= ub:
        print("wrong")
    Pi[v] = (ub + lb) / 2
    pass

print(Pi)
# Pi = [0, 1.29817, 1.65616, 3.014, 3.252655]

print(np.array(embed_with(Pi, d)))
