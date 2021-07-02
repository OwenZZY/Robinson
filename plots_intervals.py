import matplotlib.pyplot as plt
import numpy as np

def timelines(y, xstart, xstop, color='b'):
    """Plot timelines at y from xstart to xstop with given color."""
    plt.hlines(y, xstart, xstop, color, lw=4)
    plt.vlines(xstart, y+0.03, y-0.03, color, lw=2)
    plt.vlines(xstop, y+0.03, y-0.03, color, lw=2)

def min_at(arr):
    """ the input sps looks like
    arr = [L1[anc[0]], R1[anc[1], ....]]
    so return an index means at which row, it is the min
    """
    ret = 0
    for i in range(len(arr)):
        if arr[ret]< arr[i]:
            ret = i
    return ret
# N = 5
# eps = 0.0001
# L1 = [1, 1+eps+eps, 1+4 * eps, 2, 2+ eps]
# R1 = [L1[0]+2,L1[1]+4,L1[2]+4,L1[3]+3,L1[4]+3]
# L2 = [1+eps,1+eps+eps+eps, 2, 3,  4 ]
# R2 = [L2[0]+1, L2[1]+2,L2[2]+2,L2[3]+2,L2[4]+1 ]
#
# T = [L1, R1, L2, R2]
#
# anc = [0 for _ in range(4)]

# while(np.array(anc)[anc<N]):
#     for i in range()
#     print(T[])


# y= N * 1.5
# for i in range(N):
#     timelines(y, L1[i], R1[i], color='r')
#     y-= 0.5
#     timelines(y, L2[i], R2[i], color='g')
#     y-= 1

embedding = [3.97524e-05, 1.99994e+00, 2.99998e+00, 4.99995e+00, 5.99992e+00]
d = [4.00006e+00, 2.00009e+00]

L1 = []
R1 = []
L2 = []
R2 = []
y = 5
for i in range(5):
    L1.append(embedding[i]-d[0]/2)
    R1.append(embedding[i]+d[0]/2)
    timelines(y, L1[i] , R1[i],  'r')
    y -= 0.3
    L2.append(embedding[i] - d[1] / 2)
    R2.append(embedding[i] + d[1] / 2)
    timelines(y, L2[i], R2[i], 'g')
    y -= 0.7
print(np.array([L1,R1, L2, R2]))
plt.show()