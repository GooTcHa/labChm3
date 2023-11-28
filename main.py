import copy
import math
import random

eps = 0.000001

#нициализируем матрицу А
def fill_matrix(A: list, size: int):
    for i in range(size):
        A.append([])
        for j in range(size):
            A[i].append(0)
    for i in range(size):
        for j in range(i, size):
            if i == j:
                A[i][j] = i
            else:
                num = i + random.randint(1, 5)
                A[i][j] = num
                A[j][i] = num


# ищем норму вектора в пр-ве C
def find_vector_norm(V: list):
    return max(math.fabs(i) for i in V)


#находим разность векторов
def get_difference_of_vectors(V1: list, V2: list):
    return [i - j for i, j in zip(V1, V2)]


#создаём матрицу U
def create_ortogonal(A: list, x_y: list) -> list:
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


#ищем максимальный по модулю элемент
def get_max_element_coordinates(A: list, size: int):
    m = 0.0
    for i in range(size):
        for j in range(i + 1, size):
            if math.fabs(A[i][j]) > math.fabs(m):
                m = A[i][j]
                x_y = [i, j]
    return x_y


# получаем обратную матрицу
def find_inverse_matrix(U: list, x_y: list):
    U[x_y[0]][x_y[1]] *= -1
    U[x_y[1]][x_y[0]] *= -1
    return U


#Умножаем вектор на число
def multiply_vector_to_number(V: list, a):
    return [i*a for i in V]


#перемножаем матрицы
def multiply_matrix(A: list, B: list, size: int) -> list:
    res = []
    s = 0
    for i in range(size):
        res.append([])
        for j in range(size):
            for k in range(size):
                s += A[i][k] * B[k][j]
            res[i].append(s)
            s = 0
    return res


#перемножаем матрицу и вектор
def multiply_matrix_to_vector(M: list, V: list) -> list:
    res = []
    s = 0
    for i in range(len(V)):
        for j in range(len(V)):
            s += M[i][j] * V[j]
        res.append(s)
        s = 0
    return res


#вычисляем l для степенного метода
def find_lambda(y_0, y_1):
    return sum(a*b for a, b in zip(y_0, y_1))/sum(a*a for a in y_0)


#находим собственные значения для степянного метода
def find_eigenvectors(V: list, size: int):
    vectors = []
    for i in range(size):
        y = [0] * size
        y[i] = 1
        vectors.append(multiply_matrix_to_vector(V, y))
    return vectors


#решение задачи степянным методом
def find_spin_method_solution(A: list, size: int):
    V = []
    #создаём единичный вектор V для сохранения произведенией V1*V2....
    for i in range(size):
        V.append([])
        for j in range(size):
            if i == j:
                V[i].append(1)
            else:
                V[i].append(0)
    while True:
        #ищем координаты максимального по модулю элемента
        x_y = get_max_element_coordinates(A, size)
        #запоминаем максимальный по модулю эелемент
        m = A[x_y[0]][x_y[1]]
        #Проверяем отклонение итерации
        if math.fabs(m) > eps:
            #создаём ортогональную матрицу
            U = create_ortogonal(A, x_y)
            #находим к ней обратную
            U_i = find_inverse_matrix(copy.deepcopy(U), x_y)
            #запоминаем V(и сразу находим произведение правых матриц)
            V = multiply_matrix(V, U, size)
            #Находим очередное приближение
            A = multiply_matrix(multiply_matrix(U_i, A, size), U, size)
        else:
            #возвращаем полученную матрицу и собственные вектора соответствующие ей
            return A, find_eigenvectors(V, size)


#нормируем вектор
def normise_vector(V: list):
    m = find_vector_norm(V)
    return [i/m for i in V]


#решение степенным методом
def get_power_method_solutions(A: list, size: int):
    y_0 = [0] * size
    y_0[0] = 1
    while True:
        #Находим следующий y
        y_1 = multiply_matrix_to_vector(A, y_0)
        #Нормируем его
        y_t = normise_vector(y_1)
        #Находим собственное значение
        l = find_lambda(y_0, y_1)
        #проверяем ||Ax - lx||
        dif = find_vector_norm(get_difference_of_vectors(multiply_matrix_to_vector(A, y_t), multiply_vector_to_number(y_t, l)))
        if dif < eps:
            #Возвращаем собственное(макс. по модулю) значение и его собственный вектор
            return l, y_t
        #ззапоминаем y_t
        y_0 = y_t


if __name__ == '__main__':
    size = 15
        #random.randint(10, 15)
    A = []
    fill_matrix(A, size)
    print(*A, sep='\n')
    answer = find_spin_method_solution(copy.deepcopy(A), size)
    print('Решение методом вращений:')
    for i in range(size):
        print(f'Собственное значение {answer[0][i][i]} -> Норма '
              f'{find_vector_norm(get_difference_of_vectors(multiply_matrix_to_vector(A, answer[1][i]), multiply_vector_to_number(answer[1][i], answer[0][i][i])))}->'
              f' Cобственный вектор {answer[1][i]}')
    print('\n\nРешение степенным методом:')
    answer = get_power_method_solutions(A, size)
    print(f'Собственное значение: {answer[0]} -> Норма {find_vector_norm(get_difference_of_vectors(multiply_matrix_to_vector(A, answer[1]), multiply_vector_to_number(answer[1], answer[0])))}'
          f'-> Собственный вектор: {answer[1]}')