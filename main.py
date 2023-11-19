import copy
import math
import random


def fill_matrix(A: list, size: int):
    for i in range(size):
        A.append([])
        for j in range(size):
            A[i].append(0)
    for i in range(size):
        for j in range(i, size):
            num = random.randint(0, 100)
            A[i][j] = num
            if i != j:
                A[j][i] = num


def find_eigenvalue_by_power_method(A, size, eps):
    y_0 = [[0] * size]
    y_0[0] = 1
    y_1 = [[0] * size]
    for i in range(size):
        s = 0
        for j in range(size):
            s += A[i][j]*y_0[j]


def create_ortogonal(A:list, x_y: list) -> list:
    p = 2 * A[x_y[0]][x_y[1]]/(A[x_y[0]][x_y[0]] - A[x_y[1]][x_y[1]])
    cos = math.sqrt(0.5 * (1 + 1/(math.sqrt(1 + math.pow(p, 2)))))
    sin = math.copysign(math.sqrt(1 - math.pow(cos, 2)), p)
    U = []
    for i in range(size):
        U.append([0] * size)
        U[i][i] = 1
    U[x_y[0]][x_y[0]] = cos
    U[x_y[0]][x_y[1]] = -sin

    U[x_y[1]][x_y[1]] = cos
    U[x_y[1]][x_y[0]] = sin
    return U


def find_inverse_matrix(U: list, size: int, x_y: list):
    U_b = copy.deepcopy(U)
    t = copy.deepcopy(U)
    d = 1
    t[x_y[1]][x_y[1]] += t[x_y[0]][x_y[1]] * (-t[x_y[1]][x_y[0]]) / t[x_y[0]][x_y[0]]
    t[x_y[1]][x_y[0]] = 0
    for i in range(size):
        d *= t[i][i]
    U_b[x_y[0]][x_y[1]] *= -1
    U_b[x_y[1]][x_y[0]] *= -1
    for i in range(size):
        for j in range(size):
            U_b[i][j] *= d
    return U_b


def find_spin_method_solution(A: list, size: int, eps: float):
    x_y = []
    while True:
        m = 0
        for i in range(size):
            for j in range(i + 1, size):
                if math.fabs(A[i][j]) > math.fabs(m):
                    m = A[i][j]
                    x_y = [i, j]
        if math.fabs(m) > eps:
            U = create_ortogonal(A, x_y)
            U_i = find_inverse_matrix(copy.deepcopy(U), size, x_y)
        else:
            return A


if __name__ == '__main__':
    size = random.randint(10, 15)
    A = []
    eps = 0.000001
    fill_matrix(A, size)
    print(*A, sep='\n')
    find_spin_method_solution(copy.deepcopy(A), size, eps)