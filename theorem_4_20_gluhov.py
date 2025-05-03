"""
Теорема 4.20. Нечетное число N является простым тогда и только тогда, когда оно единственным образом представляется в виде разности квадратов целых неотрицательных чисел.

Любому разложению N = ab, a > b > 0 соответствует представление N = x^2 - y^2, где x = (a + b) // 2, y = (a - b) // 2.
"""

def difference_of_squares_representations(N):
    """
    Находит все представления нечетного числа N в виде разности квадратов x^2 - y^2 = N,
    где x > y >= 0, x и y — целые.
    Возвращает список кортежей (x, y).
    """
    representations = []
    for x in range((N + 1) // 2, 0, -1):
        y2 = x * x - N
        if y2 < 0:
            break
        y = int(y2 ** 0.5)
        if y * y == y2:
            representations.append((x, y))
    return representations

def is_prime_by_difference_of_squares(N):
    """
    Проверяет, является ли нечетное число N простым по теореме 4.20:
    то есть, существует ли только одно представление N = x^2 - y^2 (тривиальное: N = (N+1)//2^2 - ((N-1)//2)^2).
    """
    reps = difference_of_squares_representations(N)
    # Тривиальное представление всегда существует для нечетного N
    return len(reps) == 1

if __name__ == "__main__":
    N = int(input("Введите нечетное число N: "))
    reps = difference_of_squares_representations(N)
    print(f"Все представления {N} в виде разности квадратов:")
    for x, y in reps:
        print(f"{N} = {x}^2 - {y}^2 = {x*x} - {y*y}")
    if is_prime_by_difference_of_squares(N):
        print(f"Число {N} простое по теореме 4.20 (единственное представление).")
    else:
        print(f"Число {N} составное (несколько представлений в виде разности квадратов).") 