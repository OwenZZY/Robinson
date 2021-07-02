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


k = 3
# G = [ [ 2, 2, 1, 0, 0 ],
#       [ 2, 2, 2, 1, 1 ],
#       [ 1, 2, 2, 2, 1 ],
#       [ 0, 1, 2, 2, 2 ],
#       [ 0, 1, 1, 2, 2 ] ]
G = [[3, 2, 1, 1, 0, 0, 0],
     [2, 3, 3, 2, 1, 1, 0],
     [1, 3, 3, 2, 1, 1, 0],
     [1, 2, 2, 3, 2, 2, 1],
     [0, 1, 1, 2, 3, 2, 1],
     [0, 1, 1, 2, 2, 3, 2],
     [0, 0, 0, 1, 1, 2, 3 ]]
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



#exit(0)

print("Linear program")
U = R.U_at(R.alpha)
L = R.L_at(R.alpha)

print(U, "\n", L)

A = []
b = []

for u in range(n):
      for v in range(u, u+1):
            upper_bounds_at_uv:bds.Bounds = U.getAt(u, v)
            lower_bounds_at_uv:bds.Bounds = L.getAt(u, v)
            # x = [0 for i in range(n)]

#            x[u] += -1
#            x[v] += 1
            for bound in upper_bounds_at_uv.bounds:
                  if bound == bd.Bound.zero:
                        continue
                  restriction = x + (list(-bound.d))
                  A.append(restriction)
                  b.append(0)
                  pass

            # x = [0 for i in range(n)]
            # x[u] += 1
            # x[v] += -1
            for bound in lower_bounds_at_uv.bounds:
                  if bound == bd.Bound.zero:
                        continue
                  restriction = x + (list(bound.d))
                  A.append(restriction)
                  b.append(-(10e-6))
                  pass
            pass

"""
A:
      x_0 x_1 x_2 d_1 d_2
res1
res2
...

b: b_i <- constant constrain of res1, with <= connects them
(b_i)
"""

dummy = [1 for i in range(n+k)]
print("A: ",np.array(A))
print("b: ", b)
# np.set_printoptions(precision=1)
# print(np.append(np.array(A),
#                 np.array(b).reshape((len(b),1)),
#                 axis= 1))

res = linprog(dummy,
              A_ub=A,
              b_ub=b,
              bounds=[(0, n) for _ in range(n+k)])
# print(res)
np.set_printoptions(precision=5)
print( np.array(res.x)*100000)

n = 5
A = np.zeros((n, n))

## [  2.85  23.16  44.96  81.19  87.11 117.94  73.96]
D = res.x[n:]
Pi = res.x[:n]
# print(D,Pi)
for d_t in D:
    A_i = np.zeros((n, n))
    for u in range(n):
        for v in range(n):
            if abs(Pi[u]-Pi[v])<=d_t:
                A_i[u,v]=1
    A += A_i

print(np.array(A))