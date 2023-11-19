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



if __name__ == '__main__':
    size = random.randint(10, 15)
    A = []
    eps = 0.000001
    fill_matrix(A, size)
    print(*A, sep='\n')