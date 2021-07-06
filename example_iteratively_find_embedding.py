import numpy as np
import Tools

G1 = [[1, 1, 1, 1, 0, 0, 0],
      [1, 1, 1, 1, 1, 0, 0],
      [1, 1, 1, 1, 1, 1, 0],
      [1, 1, 1, 1, 1, 1, 1],
      [0, 1, 1, 1, 1, 1, 1],
      [0, 0, 1, 1, 1, 1, 1],
      [0, 0, 0, 1, 1, 1, 1]]

G2 = [[1, 1, 1, 1, 0, 0, 0],
      [1, 1, 1, 1, 0, 0, 0],
      [1, 1, 1, 1, 1, 0, 0],
      [1, 1, 1, 1, 1, 1, 0],
      [0, 0, 1, 1, 1, 1, 1],
      [0, 0, 0, 1, 1, 1, 1],
      [0, 0, 0, 0, 1, 1, 1]]

G3 = [[1, 1, 0, 0, 0, 0, 0],
      [1, 1, 1, 0, 0, 0, 0],
      [0, 1, 1, 1, 1, 0, 0],
      [0, 0, 1, 1, 1, 1, 1],
      [0, 0, 1, 1, 1, 1, 1],
      [0, 0, 0, 1, 1, 1, 1],
      [0, 0, 0, 1, 1, 1, 1]]
n = len(G1)

G1, G2, G3 = np.array(G1), np.array(G2), np.array(G3)

k1, k2 = 2, 3
print(G1 + G2)
Pi_1_2, d_1_2 = Tools.the_complete_procedure(G1 + G2, n=n, k=k1)
G_1_2 = Tools.embed_with(Pi_1_2, d_1_2, n)
print(G_1_2 == G1 + G2)
print("==================")

print(G2 + G3)
Pi_2_3, d_2_3 = Tools.the_complete_procedure(G2 + G3, n=n, k=k1)
G_2_3 = Tools.embed_with(Pi_2_3, d_2_3, n)
print(G_2_3 == G2 + G3)
print("==================")

print(G1 + G2 + G3)
Pi_123, d_123 = Tools.the_complete_procedure(G1 + G2 + G3, n=n, k=k2)
G_123 = Tools.embed_with(Pi_123, d_123, n)
print(G_123 == G1 + G2 + G3)
