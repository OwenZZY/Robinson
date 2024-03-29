import Tools
import Bound
import numpy as np

k = 2
G = []

# G = [[2 ,  2 , 0 , 0 , 0 , 0 , 0], # not embeddable
#     [2 , 2 , 2 , 1 , 1 , 1 , 1],
#     [0 , 2 , 2 , 2 , 1 , 1 , 1],
#     [0 , 1 , 2 , 2 , 2 , 1 , 1],
#     [0 , 1 , 1 , 2 , 2 , 2 , 1],
#     [0 , 1 , 1 , 1 , 2 , 2 , 2 ],
#     [0 , 1 , 1 , 1 , 1 , 2 , 2]]
G = [ #  embeddable
    [2, 2, 1, 1, 1, 1],
    [2, 2, 2, 1, 1, 1],
    [1, 2, 2, 2, 1, 1],
    [1, 1, 2, 2, 2, 1],
    [1, 1, 1, 2, 2, 2],
    [1, 1, 1, 1, 2, 2]]
# G = [[2, 2, 1, 0, 0, 0],
#      [2, 2, 2, 1, 1, 1],
#      [1, 2, 2, 2, 1, 1],
#      [0, 1, 2, 2, 2, 1],
#      [0, 1, 1, 2, 2, 2],
#      [0, 1, 1, 1, 2, 2]] # not embeddable
# G = [[2, 2, 1, 0, 0], # embedable
#      [2, 2, 2, 1, 1],
#      [1, 2, 2, 2, 1],
#      [0, 1, 2, 2, 2],
#      [0, 1, 1, 2, 2]]
G = [[2, 2, 2, 1, 0, 0], #
     [2, 2, 2, 1, 0, 0],
     [2, 2, 2, 2, 1, 1],
     [1, 1, 2, 2, 2, 1],
     [0, 0, 1, 2, 2, 2],
     [0, 0, 1, 1, 2, 2]]

n = len(G)
Pi, d = Tools.the_complete_procedure(G, n, k)

print("Pi = ", Pi)
print(Tools.embed_with(Pi, d, n))
