import scipy

import Bounds as bds
import Bound as bd
import Table as tbl
import UpperBounds as ubds
import LowerBounds as lbds
import Robinson as Rob
import numpy as np
from scipy.optimize import linprog



bd.Bound.zero = bd.Bound(path=[],ds=[0,0])

# G = [ [ 2, 2, 1, 0, 0, 0 ],
#       [ 2, 2, 2, 1, 1, 1 ],
#       [ 1, 2, 2, 2, 1, 1 ],
#       [ 0, 1, 2, 2, 2, 1 ],
#       [ 0, 1, 1, 2, 2, 2 ],
#       [ 0, 1, 1, 1, 2, 2 ] ]
# R = Rob.Robinson(G,  k = 2)
# R.find_embedding()


k = 2
G = [ [ 2, 2, 1, 0, 0 ],
      [ 2, 2, 2, 1, 1 ],
      [ 1, 2, 2, 2, 1 ],
      [ 0, 1, 2, 2, 2 ],
      [ 0, 1, 1, 2, 2 ] ]
# G = [[2,2,1],
#      [2,2,2],
#      [1,2,2]]
n = len(G)

R = Rob.Robinson(G,  k = k)
found = R.find_embedding()

if not found:
      print("Not embeddable")
      exit(0)
print("Claim: embeddable")

U = R.U_at(R.alpha).table
L = R.L_at(R.alpha).table

scalar_upperbd = [[[] for _ in range(n) ] for _ in range(n) ]
scalar_lowerbd = [[[] for _ in range(n) ] for _ in range(n) ]



# d = np.array([1,1.1/3]) # works
d=[1, 0.8] # does not work
#d = np.array([1, 1.1/3])
for u in range(n):
    for v in range(u, n):
        B_uv = U[u][v].bounds
        for b in B_uv:
            scalar = np.dot(b.d,d)
            if not (scalar in scalar_upperbd[u][v]):
                scalar_upperbd[u][v].append(scalar)
        B_uv = L[u][v].bounds
        for b in B_uv:
            scalar = np.dot(b.d, d)
            if not (scalar in scalar_lowerbd[u][v]):
                scalar_lowerbd[u][v].append(np.dot(b.d,d))


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


scalar_upperbd = [[[0.8, 0.2, 1.4],[0.8],[1.0, 1.6],[1.8, 2.4],[1.8, 3.2]],
[[] ,[0.8, 0.2, 1.4],[0.8, 0.2],[1.0, 1.6],[1.0, 2.4]],
[[] ,[] ,[0.8, 0.2, 1.4],[0.8],[1.0, 1.6]],
[[] ,[] ,[] ,[0.8, 0.2, 1.4],[0.8, 0.2]],
[[] ,[] ,[] ,[] ,[0.8, 0.2, 2.2]]]
scalar_lowerbd = [[[0.0, -1.4],	[0.0, 0.6, -0.6],	[0.8, 0.2],	[1.0, 1.4],	[1.0, 1.6]],
[[], 	[0.0, -1.4],	[0.0, -0.6],	[0.8, 0.2],	[0.8, 0.2]	],
[[], 	[],	[0.0, -1.4],	[0.0, -0.6, 0.6],	[0.8, -0.6]	],
[[], 	[], 	[] ,	[0.0, -1.4],	[0.0, -1.4]	],
[[], 	[], 	[] ,	[] ,	[0.0, -2.2]]]

print((scalar_upperbd), "\n", (scalar_lowerbd))
n=5
eps = 3
for i in range(n):
    for j in range(i,n):
        for ub in scalar_upperbd[i][j]:
            for lb in scalar_lowerbd[i][j]:
                if (ub-lb)<=eps:
                    print(i,",",j,": ",  ub-lb)
                    eps = ub-lb

eps = 0.201
print("eps=", eps)



Pi=[0,0,0,0,0]
Pi[0]=0
for v in range(1, n):
    Pi[v] = max([Pi[i]+ max(scalar_lowerbd[i][v]) for i in range(v)]) + (eps/2)
# Pi= [0, 0.601, 0.801, 1.402, 1.601]
d=[1, 0.8]
# for v in range(1,n):
#     Pi[v] = Pi[0]+ max(scalar_lowerbd[0][v]) + eps/2
# Pi[1]=max(scalar_lowerbd[0][1]) + eps/2
# Pi[2]=max(scalar_lowerbd[0][2]) + eps/2
# Pi[3]=max(scalar_lowerbd[0][3]) + eps/2
# Pi[4]=max([Pi[i]+ max(scalar_lowerbd[i][4]) for i in range(n)]) + eps/2 #=1.06#scalar_lowerbd[0][4][0] + eps/2
print("Pi=", Pi)
print("D=", d)
A = np.zeros((n, n))
for d_t in d:
    A_i = np.zeros((n, n))
    # print(d_t)
    for u in range(n):
        for v in range(n):
            if (abs(Pi[u]-Pi[v])<=d_t):
                A_i[u,v]=1
    print(A_i)
    A += A_i

print(np.array(A))