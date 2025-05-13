import random
import math

# Алгоритм 6.4: разложение нечетного составного числа N на нетривиальные делители

def primes_up_to(n):
    """Возвращает список всех простых чисел ≤ n."""
    sieve = [True] * (n+1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def compute_T(N, B):
    """
    Вычисляет T по формуле: произведение q_i^{r_i}, где q_i ≤ B, r_i — макс. степень, чтобы q_i^{r_i} ≤ N. 
    Можно взять T = B! 
    """
    T = 1
    for q in primes_up_to(B):
        r = 1
        while q**(r+1) <= N:
            r += 1
        T *= q**r
    return T

def factorize(N, B, T, max_failures=5):
    """
    Реализация алгоритма 6.4 для разложения нечетного составного числа N на нетривиальные делители.
    Добавлено уменьшение B, если для нескольких случайных a выполняется N1 = N.
    N: нечетное составное число
    B: положительное целое число (граница гладкости)
    T: произведение простых степеней (B-гладкое число)
    max_failures: сколько раз подряд можно получить N1 = N, прежде чем уменьшить B
    Возвращает нетривиальный делитель N или None, если не найден.
    """
    failures = 0  # Счетчик неудачных попыток (N1 = N)
    while True:
        # Шаг 1. Выбрать случайный вычет a ∈ Z_N и вычислить d = gcd(a, N)
        a = random.randrange(2, N)
        d = math.gcd(a, N)
        if 1 < d < N:
            # Если 1 < d < N, то найден нетривиальный делитель N
            print("d")
            return d

        elif d == 1:
            # Если d = 1, то вычислить b = a^T - 1 (mod N)
            b = pow(a, T, N) - 1
            b %= N
            # Шаг 2. Вычислить N1 = gcd(b, N)
            N1 = math.gcd(b, N)
            if N1 == 1:
                # Если N1 = 1, то увеличить B
                B += 1
                T = compute_T(N, B)
                failures = 0  # сбросить счетчик неудач
            elif N1 == N:
                # Если N1 = N, то увеличить счетчик неудач
                failures += 1
                if failures >= max_failures:
                    # Если для нескольких случайных a выполняется N1 = N, уменьшить B
                    B = max(2, B // 2)
                    T = compute_T(N, B)
                    failures = 0
                continue
            else:
                # Если 1 < N1 < N, то найден нетривиальный делитель N
                print("N1")
                return N1

def choose_B(N):
    """
    Автоматический выбор параметра B в зависимости от размера N.
    Обычно 10^5 < B < 10^6. Можно взять, например, B = min(max(10**5, int(N**0.2)), 10**6)
    """
    return min(max(10**5, int(N**0.2)), 10**6)

if __name__ == "__main__":
    N = int(input("Введите нечетное составное число N: "))

    B = 1000

    print(f"Автоматически выбранное значение B: {B}")
    T = compute_T(N, B)
    print(f"T вычислено. Количество цифр в T: {len(str(T))}")
    result = factorize(N, B, T)
    if result:
        print(f"Нетривиальный делитель числа {N}: {result}")
    else:
        print("Не удалось найти нетривиальный делитель.") 