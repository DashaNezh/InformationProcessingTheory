def modinv(a, m):
    # Обратное по модулю (расширенный алгоритм Евклида)
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def algorithm_1_2(x, y, N, beta, n):
    # x — число, y — число, N — модуль, beta — основание, n — количество разрядов
    x_digits = []
    temp = x
    for _ in range(n):
        x_digits.append(temp % beta)
        temp //= beta

    # Находим N', обратное к -N по модулю beta
    from math import gcd
    if gcd(-N % beta, beta) != 1:
        raise Exception(f'Параметры не подходят: -N % beta = {-N % beta} и beta = {beta} не взаимно просты')
    N_inv = modinv(-N % beta, beta)

    z = 0
    for i in range(n):
        u = (z + x_digits[i] * y) % beta
        v = (u * N_inv) % beta
        z = (z + x_digits[i] * y + v * N) // beta

    if z < N:
        return z
    else:
        return z - N

def montgomery_reduce(T, N, R, N_inv):
    m = ((T % R) * N_inv) % R
    t = (T + m * N) // R
    if t >= N:
        t -= N
    return t

def montgomery_mul(a, b, N, R, N_inv, beta, n):
    # Используем algorithm_1_2 для умножения по модулю N
    T = algorithm_1_2(a, b, N, beta, n)
    return montgomery_reduce(T, N, R, N_inv)

def montgomery_pow(x, k, N, beta, n):
    R = beta ** n
    R_inv = modinv(R, N)
    N_inv = -modinv(N, R) % R

    x_mont = algorithm_1_2(x, R % N, N, beta, n)
    one_mont = algorithm_1_2(1, R % N, N, beta, n)

    result = one_mont
    while k > 0:
        if k % 2 == 1:
            result = montgomery_mul(result, x_mont, N, R, N_inv, beta, n)
        x_mont = montgomery_mul(x_mont, x_mont, N, R, N_inv, beta, n)
        k //= 2

    # Переводим результат обратно из Монтгомери-формы
    result = algorithm_1_2(result, R_inv, N, beta, n)
    return result

# Алгоритм 1.1: Монтгомери-редукция
def algorithm_1_1(x, N, R, N_inv):
    m = (x * N_inv) % R
    t = (x + m * N) // R
    if t < N:
        return t
    else:
        return t - N

def pow_via_algorithms(x, k, N, beta, n):
    R = beta ** n
    N_inv = -modinv(N, R) % R

    # Шаг 1: y1 = algorithm_1_2(x, R % N, N, beta, n)
    y = algorithm_1_2(x, R % N, N, beta, n)

    # Шаги 2..k: y = algorithm_1_2(y, x, N, beta, n)
    for _ in range(1, k):
        y = algorithm_1_2(y, x, N, beta, n)

    # Шаг k+1: algorithm_1_1(y, N, R, N_inv)
    result = algorithm_1_1(y, N, R, N_inv)
    return result

# Пример использования алгоритма возведения в степень
x = 5
k = 3
N = 13
beta = 2
n = 4  # R = 16 > 13

print("С помощью алгоритмов: ", pow_via_algorithms(x, k, N, beta, n))  # Должно вывести 8

print("Проверка: ", 5**3 % 13)