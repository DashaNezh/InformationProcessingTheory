# Программа реализует эффективный алгоритм возведения в степень по модулю (x^k mod N)
# с использованием метода Монтгомери

def modinv(a, m):
    """
    Находит обратное число по модулю m для числа a.
    Использует расширенный алгоритм Евклида.
    """

    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def extended_gcd(a, b):
    """
    Расширенный алгоритм Евклида.
    Возвращает НОД и коэффициенты Безу.
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


def algorithm_1_2(x, y, N, beta, n):
    """
    Алгоритм умножения по модулю N.
    x, y - числа для умножения
    N - модуль
    beta - основание системы счисления
    n - количество разрядов
    """
    # Разбиваем число x на разряды в системе счисления с основанием beta
    x_digits = []
    temp = x
    for _ in range(n):
        x_digits.append(temp % beta)
        temp //= beta

    # Проверяем, что -N и beta взаимно просты
    from math import gcd
    if gcd(-N % beta, beta) != 1:
        raise Exception(f'Параметры не подходят: -N % beta = {-N % beta} и beta = {beta} не взаимно просты')

    # Находим обратное к -N по модулю beta
    N_inv = modinv(-N % beta, beta)

    # Основной цикл умножения
    z = 0
    for i in range(n):
        u = (z + x_digits[i] * y) % beta
        v = (u * N_inv) % beta
        z = (z + x_digits[i] * y + v * N) // beta

    # Возвращаем результат по модулю N
    if z < N:
        return z
    else:
        return z - N


def algorithm_1_1(x, N, R, N_inv):
    """
    Алгоритм Монтгомери-редукции.
    Преобразует число из формы Монтгомери обратно в обычную форму.
    """
    m = (x * N_inv) % R
    t = (x + m * N) // R
    if t < N:
        return t
    else:
        return t - N


def pow_via_algorithms(x, k, N, beta, n):
    """
    Возведение в степень по модулю N с использованием алгоритмов 1.1 и 1.2.
    """
    R = beta ** n
    N_inv = -modinv(N, R) % R

    # Преобразуем число в форму Монтгомери
    y = algorithm_1_2(x, R % N, N, beta, n)

    # Выполняем умножение k-1 раз
    for _ in range(1, k):
        y = algorithm_1_2(y, x, N, beta, n)

    # Возвращаем результат из формы Монтгомери
    result = algorithm_1_1(y, N, R, N_inv)
    return result


# Пример использования алгоритма
x = 7  # число для возведения в степень
k = 3  # показатель степени
N = 13  # модуль
beta = 2  # основание системы счисления
n = 4  # количество разрядов (R = 16 > 13)

print("С помощью алгоритмов: ", pow_via_algorithms(x, k, N, beta, n))  # Должно вывести 8

print("Проверка: ", 7 ** 3 % 13)
