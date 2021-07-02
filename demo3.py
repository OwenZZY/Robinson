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
n = len(G)

Bound.Bound.zero = Bound.Bound(path=[], ds=[0 for _ in range(k)])

UBW, LBW = Tools.Bound_Generation_mod(G, n, k)

contradiction_exists = False
for i in range(n):
    for j in range(n):
        if LBW[i][j].causes_contradiction(UBW[i][j]):
            print("Causes Contradiction at (", i, ",", j, ")")
            contradiction_exists = True
if contradiction_exists:
    exit(0)

Tools.compute_cycles(UBW=UBW, LBW=LBW, n=n)

LinProg = Tools.construct_and_compute_linear_program(UBW, LBW, n, k)

if LinProg.x[k] <= 0:
    print("No solution, z<0")
    exit(0)

readable_solution = Tools.scale_to_readable_numbers(LinProg.x)
print("[d_1, d_2, ..., d_k, z] = ", readable_solution,"\n")
d = np.array(readable_solution[:-1])

scalar_upperbd, scalar_lowerbd = Tools.compute_scalar_bounds(UBW, LBW, n=n, d=d)
# print(np.array(scalar_lowerbd))
# print(np.array(scalar_upperbd))

Pi = Tools.compute_a_uniform_embedding(scalar_upperbd, scalar_lowerbd, n)
print("Pi = ", Pi)
print(Tools.embed_with(Pi, d, n))
