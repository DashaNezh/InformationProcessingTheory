import math

def integer_sqrt(N):
    """
    Алгоритм 2.6: Вычисление целой части квадратного корня из N.
    Возвращает floor(sqrt(N)).
    """
    x = N
    while True:
        xi = (x + N // x) // 2
        if xi >= x:
            return x
        x = xi

def fermat_factorization(N):
    """
    Алгоритм Ферма для разложения нечетного числа N на нетривиальные делители.
    Возвращает кортеж (a, b), если разложение найдено, иначе None.
    """
    assert N % 2 == 1, "N должно быть нечетным"
    x = integer_sqrt(N)
    if x * x < N:
        x += 1
    while x <= (N + 1) // 2:
        t = x * x - N
        if t < 0:
            x += 1
            continue
        y = integer_sqrt(t)
        if y * y == t:
            a = x + y
            b = x - y
            if a == 1 or b == 1:
                x += 1
                continue
            return a, b
        x += 1
    return None

if __name__ == "__main__":
    N = int(input("Введите нечетное составное число N: "))
    result = fermat_factorization(N)
    if result:
        print(f"{N} = {result[0]} * {result[1]}")
    else:
        print("Не удалось разложить число на нетривиальные делители.")
