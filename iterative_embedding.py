import Bound as bd
import Robinson as Rob
import numpy as np

def embed_with(Pi, d):
    print("Pi=", Pi)
    print("D=", d)
    A = np.zeros((n, n))
    for d_t in d:
        A_i = np.zeros((n, n))
        # print(d_t)
        for u in range(n):
            for v in range(n):
                if abs(Pi[u] - Pi[v])<=d_t:
                    A_i[u,v]=1
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
bd.Bound.zero = bd.Bound(path=[],ds=[0 for _ in range(k)])
# G = [[3, 2, 1, 1, 0, 0, 0],
#      [2, 3, 3, 2, 1, 1, 0],
#      [1, 3, 3, 2, 1, 1, 0],
#      [1, 2, 2, 3, 2, 2, 1],
#      [0, 1, 1, 2, 3, 2, 1],
#      [0, 1, 1, 2, 2, 3, 2],
#      [0, 0, 0, 1, 1, 2, 3 ]]
G = [ [ 2, 2, 1, 0, 0 ],
      [ 2, 2, 2, 1, 1 ],
      [ 1, 2, 2, 2, 1 ],
      [ 0, 1, 2, 2, 2 ],
      [ 0, 1, 1, 2, 2 ] ]
#
# G = [ [ 2, 2, 1, 0, 0, 0 ],
#       [ 2, 2, 2, 1, 1, 1 ],
#       [ 1, 2, 2, 2, 2, 1 ],
#       [ 0, 1, 2, 2, 2, 2 ], # copied vertex
#       [ 0, 1, 2, 2, 2, 2 ], # new vertex
#       [ 0, 1, 1, 2, 2, 2 ] ]

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

# d = np.array([2.1703,  1.18741, 0.05664])

# d = np.array([2.01415, 1.53683])
d = np.array([2, 1.5])
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

# useless, just printing
for u in range(n):
    for v in range(n):
        if v<u:
            print("[] ",end="\t")
        else:
            print(scalar_upperbd[u][v],end="\t")
    print()
print()
for u in range(n):
    for v in range(n):
        if v<u:
            print("[] ",end="\t")
        else:
            print(scalar_lowerbd[u][v],end="\t")
    print()

Wrong = False
for u in range(n):
    for v in range(u,n):
        if max(scalar_lowerbd[u][v]) > min(scalar_upperbd[u][v]):
            print("Contradiction at: (", u ,",", v,"):", max(scalar_lowerbd[u][v]), ",", min(scalar_upperbd))
            Wrong = True
print("There is ", end="")
if not Wrong: print("no ", end="")
print("wrong\n")


Pi=[0 for _ in range(n)]
Pi[0]=0

for v in range(1,n):
    lb = max([Pi[i]+ max(scalar_lowerbd[i][v]) for i in range(v)])
    ub = min([Pi[i]+ min(scalar_upperbd[i][v]) for i in range(v)])
    if lb>=ub:
        print("wrong")
    Pi[v] = (ub+lb)/2
    pass

print(Pi)
# Pi = [0, 1.29817, 1.65616, 3.014, 3.252655]

print(np.array(embed_with(Pi, d)))