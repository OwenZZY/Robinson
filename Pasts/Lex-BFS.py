

# target:
# given a set of random list of G
# sort

import numpy as np

def N(v, G)->list:
    ret = []
    for u in range(len(G)):
        if u==v:
            pass
        if G[u][v]==1:
            ret.append(u)
    return ret

def lexBFS(G, sigma:list):
    H = [sigma]
    I = []
    n = len(G)
    for _ in range(n):
        Hp = []
        u = H[0][0]
        H[0].pop(0)
        if len(H[0])==0:
            H.pop(0)
        I.append(u)
        print(I)
        for h in H:
            S=[]
            T=[]
            for v in h:
                if G[u][v]!=0:
                    S.append(v)
                else:
                    T.append(v)
            if len(S)!=0:
                Hp.append(S)
            if len(T)!=0:
                Hp.append(T)
        H = Hp
        print(H)
    return I

#np.random.permutation(10)

n=10
G = [[0 for i in range(n)] for j in range(n)]
for i in range(n):
    for j in range(n):
        if abs(i-j)<5:
            G[i][j]=1
print(np.array(G))
#sigma = [4, 9, 7, 2, 5, 3, 0, 6, 1, 8] #
sigma =  np.random.permutation(n)
sigma = sigma.tolist()

print(sigma)
sigma.reverse()
sigma_p = lexBFS(G,sigma)
sigma_p.reverse()
sigma_pp = lexBFS(G, sigma_p)

print(sigma_pp)


to = 0
pi = [sigma_pp][0]
Perm = [[0 for _ in range(n)]for _ in range(n)]
for total in range(n):
    if pi[to]==-1 and total<n:
        # print("to: ", to)
        for t in range(n):
            if pi[t]!=-1:
                to=t
                break
    Perm[to][pi[to]] = 1
    # Perm[pi[to]][to] = 1
    oldto = to
    to=pi[to]
    pi[oldto] = -1

# print(np.array(Perm))
# print(pi)

G = np.array(G)
Perm = np.array(Perm)

R = Perm.T @ G @ Perm
print(R)