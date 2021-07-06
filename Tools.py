import sys
from scipy.optimize import linprog

import Bound
import Bounds
import LowerBounds
import UpperBounds
import numpy as np

""" 
:param G    the adjacency matrix of a graph
:param n    the size of the graph 
:param k    the number of levels in the graph
:return Pi  the embedding of a graph
:return d   if k!=2, then d is the computed threshold vector of a graph
            if k==2, then d is k pairs of range
"""


def the_complete_procedure(G, n, k):
    Bound.Bound.zero = Bound.Bound(path=[], ds=[0 for _ in range(k)])

    UBW, LBW = Bound_Generation_mod(G, n, k)

    if UBW == False:
        return

    contradiction_exists = False
    for i in range(n):
        for j in range(n):
            if LBW[i][j].causes_contradiction(UBW[i][j]):
                print("Causes Contradiction at (", i, ",", j, ")")
                contradiction_exists = True
    if contradiction_exists:
        exit(0)

    compute_cycles(UBW=UBW, LBW=LBW, n=n)

    # if k == 2:
    #     print("Do something")
    #     pass
    if k != 0:
        print("\nStart constructing a linear program, note linprog maximizes elements wrt -Ad<=0..")
        LinProg = compute_linear_program(UBW, LBW, n, k)

        if LinProg.x[k] <= 0:
            print("No solution, z<0")
            exit(0)

        readable_solution = scale_to_readable_numbers(LinProg.x)
        print("[d_1, d_2, ..., d_k, z] = ", readable_solution, "\n")
        d = np.array(readable_solution[:-1])

        scalar_upperbd, scalar_lowerbd = compute_scalar_bounds(UBW, LBW, n=n, d=d)
        # print(np.array(scalar_lowerbd))
        # print(np.array(scalar_upperbd))
    else:
        scalar_upperbd, scalar_lowerbd = None, None

    Pi = compute_a_uniform_embedding(scalar_upperbd, scalar_lowerbd, n)
    return Pi, d


def construct_the_constrain_matrix(UBW, LBW, n, k):
    ConstrainMatrix = []
    for i in range(n):
        for B in UBW[i][i].getBounds():
            constrain = list(B.get_array()[:])
            constrain.append(-1)
            if ConstrainMatrix.__contains__(constrain):
                continue
            ConstrainMatrix.append(constrain)
    for k_ in range(k - 1):
        constrain = [0 for _ in range(k + 1)]
        constrain[-1] = -1
        constrain[k_] = 1
        constrain[k_ + 1] = -1
        if ConstrainMatrix.__contains__(constrain):
            continue
        ConstrainMatrix.append(constrain)
    constrain = [0 for _ in range(k + 1)]
    constrain[-1] = -1
    constrain[-2] = 1
    if ConstrainMatrix.__contains__(constrain):
        pass
    ConstrainMatrix.append(constrain)
    return ConstrainMatrix


def compute_linear_program(ConstrainMatrix, k):
    Zeros = [0 for _ in range(len(ConstrainMatrix))]
    dummy = [0 for _ in range(k + 1)]
    dummy[-1] = -1
    # print("Dummy variable", dummy)
    # print("Constrain matrix, Ax -z >= 0\n", np.array(ConstrainMatrix))
    # print("Modify the Constrain matrix, and get -Ax +z <=0 \n", -np.array(ConstrainMatrix))
    # print("Zeros as upper bounds\n", list(Zeros))

    variable_ranges = [(0, None) for _ in range(k + 1)]
    variable_ranges[k] = (-.1, .1)
    LinProg = linprog(dummy,
                      A_ub=-np.array(ConstrainMatrix),
                      b_ub=list(Zeros),
                      bounds=variable_ranges)

    print("Linear Program multiplied solution: \n", np.dot(np.array(ConstrainMatrix), LinProg.x))
    print("\nLinear program computed, print result: \n", np.array(LinProg.x), "\n")
    return LinProg


def add_bound_to(theTable: list, theBounds: Bounds, at_i: int, at_j: int):
    for bs in theBounds.getBounds():
        theTable[at_i][at_j].union(bs)


def no_contradiction(Us, Ls, n) -> (int, int):
    for i in range(n):
        for j in range(i, n):
            if Ls[i][j].causes_contradiction(Us[i][j]):
                print(str(Ls[i][j]), " versus ", Us[i][j])
                return i, j
    return -1, -1


def ends_match(l1: list, l2: list):
    if l1[len(l1) - 1] != l2[0]:
        print("Error, concat fail", l1, l2)
        exit(0)
        return False
    return True


def contain_repeating_vertices(Walk: list):
    if len(Walk) == len(set(Walk)):
        return False
    return True


def embed_with(Pi, d, n):
    # print("Pi=", Pi)
    # print("D=", d)
    A = np.zeros((n, n))
    for d_t in d:
        A_i = np.zeros((n, n))
        # print(d_t)
        for u in range(n):
            for v in range(n):
                if abs(Pi[u] - Pi[v]) <= d_t:
                    A_i[u, v] = 1
        # print(A_i)
        A += A_i
    return A


'''
Robinson matrix A in S^n[k]
'''


def Bound_Generation_mod(G: list, n, k):
    UBW = [[UpperBounds.UpperBounds() for _ in range(n)] for _ in range(n)]
    LBW = [[LowerBounds.LowerBounds() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i, n):
            # construct upper bound on (i, j)
            if G[i][j] != 0:
                b_plus_ij = [0 for _ in range(k)]
                b_plus_ij[G[i][j] - 1] = 1
                UBW[i][j].union(Bound.Bound(path=[i, j], ds=b_plus_ij))

            # construct lower bound on (i, j)
            b_minus_ij = [0 for _ in range(k)]
            if G[i][j] < k:
                b_minus_ij[G[i][j]] = 1
            LBW[i][j].union(Bound.Bound(path=[i, j], ds=b_minus_ij))
    print("Initialization completed..")
    # for i in range(n):
    #     for j in range(i, n):
    #         print("(", str(i), ",", str(j), "): ", UBW[i][j], "\t", end='')
    #     print("")
    # print("\n")
    # for i in range(n):
    #     for j in range(i, n):
    #         print("(", str(i), ",", str(j), "): ", LBW[i][j], "\t", end='')
    #     print("")

    for s in range(n):
        for i in range(n):
            for j in range(i, n):
                if i == s or j == s:
                    continue
                # print("(", i, ",", j, ",", s, ")")
                if i < s and s < j:
                    for B_1 in UBW[i][s].getBounds():
                        for B_2 in UBW[s][j].getBounds():
                            B_1: Bound.Bound
                            B_2: Bound.Bound
                            b_1, path_1, b_2, path_2 = B_1.get_array(), B_1.path, B_2.get_array(), B_2.path
                            b = np.array(b_1) + np.array(b_2)
                            ends_match(path_1, path_2)
                            path = path_1 + path_2[1:]
                            if contain_repeating_vertices(path):
                                continue
                            UBW[i][j].union(Bound.Bound(path=path, ds=list(b)))

                    for A_1 in LBW[i][s].getBounds():
                        for A_2 in LBW[s][j].getBounds():
                            A_1: Bound.Bound
                            A_2: Bound.Bound
                            a_1, path_1, a_2, path_2 = A_1.get_array(), A_1.path, A_2.get_array(), A_2.path
                            a = np.array(a_1) + np.array(a_2)
                            ends_match(path_1, path_2)
                            path = path_1 + path_2[1:]
                            if contain_repeating_vertices(path):
                                continue
                            LBW[i][j].union(Bound.Bound(path=path, ds=list(a)))

                if j < s:
                    for B in UBW[i][s].getBounds():
                        for A in LBW[j][s].getBounds():
                            A: Bound.Bound
                            B: Bound.Bound
                            a, path_a, b, path_b = A.get_array(), A.path, B.get_array(), B.path
                            newB = np.array(b) - np.array(a)
                            ends_match(path_b, path_a[::-1])
                            newPath = path_b + path_a[:-1][::-1]
                            if contain_repeating_vertices(newPath):
                                continue
                            UBW[i][j].union(Bound.Bound(path=newPath, ds=list(newB)))

                    for A in LBW[i][s].getBounds():
                        for B in UBW[j][s].getBounds():
                            A: Bound.Bound
                            B: Bound.Bound
                            a, path_a, b, path_b = A.get_array(), A.path, B.get_array(), B.path
                            newA = np.array(a) - np.array(b)
                            ends_match(path_a, path_b[::-1])
                            newPath = path_a + path_b[:-1][::-1]
                            if contain_repeating_vertices(newPath):
                                continue
                            LBW[i][j].union(Bound.Bound(path=newPath, ds=list(newA)))

                if i < s:
                    for A in LBW[s][i].getBounds():
                        for B in UBW[s][j].getBounds():
                            A: Bound.Bound
                            B: Bound.Bound
                            a, path_a, b, path_b = A.get_array(), A.path, B.get_array(), B.path
                            newB = np.array(b) - np.array(a)
                            ends_match(path_a[1:][::-1], path_b)
                            newPath = path_a[1:][::-1] + path_b
                            if contain_repeating_vertices(newPath):
                                continue
                            UBW[i][j].union(Bound.Bound(path=newPath, ds=list(newB)))

                    for B in UBW[s][i].getBounds():
                        for A in LBW[s][j].getBounds():
                            A: Bound.Bound
                            B: Bound.Bound
                            a, path_a, b, path_b = A.get_array(), A.path, B.get_array(), B.path
                            newA = np.array(a) - np.array(b)
                            ends_match(path_a, path_b[::-1])
                            newPath = path_b[1:][::-1] + path_a
                            if contain_repeating_vertices(newPath):
                                continue
                            LBW[i][j].union(Bound.Bound(path=newPath, ds=list(newA)))
        # print("==========iter ", s, "============")
        # for i in range(n):
        #     for j in range(i, n):
        #         print("(", str(i), ",", str(j), "): ", UBW[i][j], "\t", end='')
        #     print("")
        # print("\n")
        # for i in range(n):
        #     for j in range(i, n):
        #         print("(", str(i), ",", str(j), "): ", LBW[i][j], "\t", end='')
        #     print("")
    print("Bound-Generation-mod complete..")
    # for i in range(n):
    #     for j in range(i, n):
    #         print("(", str(i), ",", str(j), "): ", UBW[i][j], "\t", end='')
    #     print("")
    # print("\n")
    # for i in range(n):
    #     for j in range(i, n):
    #         print("(", str(i), ",", str(j), "): ", LBW[i][j], "\t", end='')
    #     print("")

    return UBW, LBW


def compute_cycles(UBW: list, LBW: list, n):
    for i in range(n):
        for j in range(i + 1, n):
            U_ij: Bounds.Bounds = UBW[i][j]
            L_ij: Bounds.Bounds = LBW[i][j]
            U_ii: Bounds.Bounds = UBW[i][i]
            # L_ii: Bounds.Bounds = LBW[i][i]

            for B in U_ij.getBounds():
                for A in L_ij.getBounds():
                    B: Bound.Bound
                    A: Bound.Bound
                    a, path_a, b, path_b = A.get_array(), A.path, B.get_array(), B.path
                    c_array = np.array(b) - np.array(a)
                    c_path = path_b + path_a[:-1][::-1]
                    U_ii.union(Bound.Bound(path=c_path, ds=c_array))
    print("Cycles computed..\n Upper Bound")

    # for i in range(n):
    #     for j in range(i, n):
    #         print("(", str(i), ",", str(j), "): ", UBW[i][j], "\t", end='')
    #     print("")
    # print("\n Lower Bound")
    # for i in range(n):
    #     for j in range(i, n):
    #         print("(", str(i), ",", str(j), "): ", LBW[i][j], "\t", end='')
    #     print("")


def scale_to_readable_numbers(X: list):
    there_is_element_less_than_one = True
    NPX = np.array(X)
    while True:
        there_is_element_less_than_one = False
        for i in range(len(NPX)):
            if NPX[i] < 1:
                there_is_element_less_than_one = True
                break
        if there_is_element_less_than_one:
            NPX = NPX * 10
        else:
            break
    return NPX


def compute_scalar_bounds(UBW, LBW, n, d):
    scalar_upperbd = [[sys.float_info.max for _ in range(n)] for _ in range(n)]
    scalar_lowerbd = [[0 for _ in range(n)] for _ in range(n)]

    for u in range(n):
        for v in range(u + 1, n):
            for b in UBW[u][v].getBounds():
                scalar = np.dot(b.d, d)
                if scalar < scalar_upperbd[u][v]:
                    scalar_upperbd[u][v] = scalar

            for b in LBW[u][v].getBounds():
                scalar = np.dot(b.d, d)
                if scalar > scalar_lowerbd[u][v]:
                    scalar_lowerbd[u][v] = scalar
    return scalar_upperbd, scalar_lowerbd


def compute_a_uniform_embedding(scalar_upperbd, scalar_lowerbd, n):
    Pi = [0 for _ in range(n)]

    for v in range(1, n):
        lb = max([(Pi[i] + scalar_lowerbd[i][v]) for i in range(v)])
        ub = min([(Pi[i] + scalar_upperbd[i][v]) for i in range(v)])
        # if lb >= ub:
        #     print(v, "wrong", lb, "\t", ub)
        Pi[v] = (ub + lb) / 2
    return Pi
