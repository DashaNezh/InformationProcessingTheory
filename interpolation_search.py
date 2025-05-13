def interpolation_search_verbose(arr, key):
    """
    Интерполяционный поиск элемента x в отсортированном массиве arr с подробным выводом шагов.
    Возвращает индекс элемента или -1, если элемент не найден.
    """
    left = 0
    right = len(arr) - 1

    while left <= right and key >= arr[left] and key <= arr[right]:
        print(f"\nШаг цикла: left={left}, right={right}")
        print(f"Значения на границах: arr[left]={arr[left]}, arr[right]={arr[right]}")

        # Проверка на равенство значений в границах
        if arr[right] == arr[left]:
            print("Границы совпали по значению.")
            if arr[left] == key:
                print(f"Элемент {key} найден на позиции {left}")
                return left
            else:
                print(f"Элемент {key} не может быть найден — все элементы равны {arr[left]}")
                return -1

        # Интерполяционная формула
        num = (key - arr[left])
        den = (arr[right] - arr[left])
        pos = left + (right - left) * num // den
        print(f"Вычисляем позицию: pos = left + (right - left) * (key - arr[left]) // (arr[right] - arr[left])")
        print(f"               = {left} + ({right} - {left}) * ({key} - {arr[left]}) // ({arr[right]} - {arr[left]})")
        print(f"               = {pos}")

        # Проверяем валидность pos
        if pos < 0 or pos >= len(arr):
            print(f"Рассчитанная позиция {pos} выходит за границы массива.")
            return -1

        # Сравнение и сдвиг границ
        print(f"Смотрим на arr[{pos}] = {arr[pos]}")
        if arr[pos] == key:
            print(f"Элемент {key} найден на позиции {pos}")
            return pos
        elif arr[pos] < key:
            print(f"{arr[pos]} < {key} → сдвигаем left на {pos + 1}")
            left = pos + 1
        else:
            print(f"{arr[pos]} > {key} → сдвигаем right на {pos - 1}")
            right = pos - 1

    print(f"Цикл завершён. Элемент {key} не найден.")
    return -1


if __name__ == "__main__":
    # Пример массива
    arr = [10, 20, 30, 40, 45, 50, 60, 70, 80, 90]
    try:
        x = int(input("Введите число для поиска: "))
    except ValueError:
        print("Пожалуйста, введите целое число.")
        exit(1)

    result = interpolation_search_verbose(arr, x)
    if result == -1:
        print("Результат: элемент не найден.")
    else:
        print(f"Результат: элемент найден по индексу {result}.")