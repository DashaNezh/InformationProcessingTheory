import numpy as np
import random
from prettytable import PrettyTable


# Класс для кодирования данных по коду Хэмминга
class HammingEncoder:
    """
    Класс для кодирования данных с использованием кода Хэмминга.

    Код Хэмминга - это метод обнаружения и исправления ошибок в передаваемых данных.
    Этот класс реализует кодирование двоичных данных с добавлением контрольных битов,
    которые позволяют обнаруживать и исправлять одиночные ошибки в передаваемых данных.
    """

    def __init__(self, debug=False):
        self.encoded_data = []
        self.debug = debug
        if self.debug:
            print("\nИнициализация кодировщика Хэмминга (режим отладки)")

    # Кодирование списка двоичных блоков
    def encode(self, data_blocks):
        """
        Кодирует список двоичных блоков с использованием кода Хэмминга.

        Для каждого блока данных:
        1. Добавляет контрольные биты в позиции степеней двойки
        2. Вычисляет значения контрольных битов
        3. Устанавливает контрольные биты в код

        Args:
            data_blocks (list): Список двоичных строк для кодирования

        Returns:
            list: Список словарей, содержащих оригинальные и закодированные данные
        """
        if self.debug:
            print("\n" + "=" * 50)
            print("НАЧАЛО ПРОЦЕССА КОДИРОВАНИЯ")
            print(f"Количество блоков для кодирования: {len(data_blocks)}")
            print("=" * 50)

        for i, block in enumerate(data_blocks):
            if self.debug:
                print(f"\nКодирование блока {i + 1}/{len(data_blocks)}")
                print(f"Исходные данные: {block} (длина: {len(block)} бит)")

            # 1. Добавление контрольных битов
            extended_block = self._insert_control_bits(block)
            if self.debug:
                print("\n1. Добавление контрольных битов:")
                print(f"Результат: {extended_block}")
                self._visualize_block(extended_block, "Блок с контрольными битами (пока нулевыми)")

            # 2. Вычисление значений контрольных битов
            control_values = self._compute_control_bits(extended_block)
            if self.debug:
                print("\n2. Вычисление контрольных битов:")
                for power, value in control_values.items():
                    print(f"Контрольный бит R{2 ** power} (позиция {2 ** power}) = {value}")

            # 3. Установка контрольных битов
            final_code = self._apply_control_bits(extended_block, control_values)
            if self.debug:
                print("\n3. Установка контрольных битов:")
                print(f"Финальный закодированный блок: {final_code}")
                self._visualize_block(final_code, "Закодированный блок")
                print("-" * 50)

            self.encoded_data.append({"original": block, "encoded": final_code})
        return self.encoded_data

    # Метод вычисления значений контрольных битов
    def _compute_control_bits(self, data):
        """
        Вычисляет значения контрольных битов для закодированных данных.

        Для каждого контрольного бита (позиции степени двойки):
        1. Определяет, какие биты данных влияют на данный контрольный бит
        2. Вычисляет четность (сумму по модулю 2) этих битов

        Args:
            data (str): Двоичная строка с добавленными контрольными битами

        Returns:
            dict: Словарь с позициями и значениями контрольных битов
        """
        control_values = {}
        if self.debug:
            print("\nПодробный расчет контрольных битов:")

        for idx, bit in enumerate(data):
            bit_position = idx + 1
            binary_pos = bin(bit_position)[2:][::-1]  # Двоичное представление в обратном порядке

            if self.debug:
                print(f"\nПозиция {bit_position} ({binary_pos[::-1]}): бит {bit}")

            for power, bit_value in enumerate(binary_pos):
                if bit_value == '1':
                    if self.debug:
                        print(f"  Влияет на контрольный бит R{2 ** power} (2^{power})")
                    control_values[power] = control_values.get(power, 0) + int(bit)

        # Вычисляем четность для каждого контрольного бита
        result = {k: v % 2 for k, v in control_values.items()}
        return result

    # Метод установки контрольных битов в соответствующие позиции
    def _apply_control_bits(self, data, control_values):
        """
        Устанавливает вычисленные значения контрольных битов в код.

        Args:
            data (str): Двоичная строка с нулевыми контрольными битами
            control_values (dict): Словарь с позициями и значениями контрольных битов

        Returns:
            str: Двоичная строка с установленными контрольными битами
        """
        data_list = list(data)
        if self.debug:
            print("\nУстановка вычисленных контрольных битов:")

        for power, value in control_values.items():
            pos = 2 ** power - 1  # Переводим в 0-based индекс
            if self.debug:
                print(f"Устанавливаем R{2 ** power} (позиция {pos + 1}) = {value}")
            data_list[pos] = str(value)

        return ''.join(data_list)

    # Добавление контрольных битов в код
    def _insert_control_bits(self, data):
        """
        Вставляет контрольные биты в исходные данные.

        Контрольные биты вставляются в позиции, которые являются степенями двойки
        (1, 2, 4, 8 и т.д.). Изначально устанавливаются в '0' и позже заменяются
        на правильные значения.

        Args:
            data (str): Исходная двоичная строка без контрольных битов

        Возвращает:
            str: Строка с добавленными контрольными битами на нужных позициях
        """
        result = ""
        data_ptr = 0
        index = 1

        if self.debug:
            print("\nПроцесс вставки контрольных битов:")

        while data_ptr < len(data) or len(result) < self._total_length(len(data)):
            if self._is_power_of_two(index):
                if self.debug:
                    print(f"Позиция {index}: вставлен контрольный бит R{index} (0)")
                result += "0"
            else:
                if data_ptr < len(data):
                    if self.debug:
                        print(f"Позиция {index}: бит данных D{index} = {data[data_ptr]}")
                    result += data[data_ptr]
                    data_ptr += 1
                else:
                    break
            index += 1

        return result

    def _total_length(self, data_length):
        # Вычисляем общую длину с контрольными битами
        m = data_length
        r = 1
        while (2 ** r) < (m + r + 1):
            r += 1
        return m + r

    def _visualize_block(self, block, title):
        print(f"\n{title}:")
        for i, bit in enumerate(block):
            pos = i + 1
            if self._is_power_of_two(pos):
                print(f"[R{pos}:{bit}]", end=" ")
            else:
                print(f"D{pos}:{bit}", end=" ")
        print()

    @staticmethod
    def _is_power_of_two(n):
        """
        Проверяет, является ли число степенью двойки.

        Args:
            n (int): Число для проверки

        Returns:
            bool: True если число является степенью двойки, иначе False
        """
        return n != 0 and (n & (n - 1)) == 0


# Класс для декодирования данных по коду Хэмминга
class HammingDecoder:
    """
    Класс для декодирования данных, закодированных кодом Хэмминга.

    Этот класс реализует:
    1. Обнаружение ошибок в закодированных данных
    2. Исправление одиночных ошибок
    3. Извлечение исходных данных из закодированного сообщения
    """

    def __init__(self, debug=False):
        self.decoded_data = []
        self.debug = debug
        if self.debug:
            print("\nИнициализация декодера Хэмминга (режим отладки)")

    # Декодирование списка двоичных блоков
    def decode(self, encoded_blocks):
        """
        Декодирует список закодированных блоков данных.

        Для каждого блока:
        1. Находит позицию ошибки (если есть)
        2. Исправляет ошибку
        3. Удаляет контрольные биты для получения исходных данных

        Args:
            encoded_blocks (list): Список закодированных двоичных строк

        Returns:
            list: Список словарей с исправленными и декодированными данными
        """
        if self.debug:
            print("\n" + "=" * 50)
            print("НАЧАЛО ПРОЦЕССА ДЕКОДИРОВАНИЯ")
            print(f"Количество блоков для декодирования: {len(encoded_blocks)}")
            print("=" * 50)

        for i, block in enumerate(encoded_blocks):
            if self.debug:
                print(f"\nДекодирование блока {i + 1}/{len(encoded_blocks)}")
                print(f"Полученные данные: {block}")
                self._visualize_block(block, "Полученный блок")

            # 1. Поиск ошибок
            error_position = self._find_error(block)
            if error_position:
                if self.debug:
                    print(f"\nОбнаружена ошибка в позиции {error_position}")
                block = self._correct_error(block, error_position)
                if self.debug:
                    print(f"Исправленный блок: {block}")
                    self._visualize_block(block, "Исправленный блок")
            else:
                if self.debug:
                    print("\nОшибок не обнаружено")

            # 2. Удаление контрольных битов
            decoded = self._remove_control_bits(block)
            if self.debug:
                print(f"\nДекодированные данные: {decoded}")
                print("-" * 50)

            self.decoded_data.append({"corrected": block, "decoded": decoded})
        return self.decoded_data

    # Поиск ошибки на основе контрольных битов
    def _find_error(self, data):
        """
        Находит позицию ошибки в закодированных данных.

        Вычисляет синдром ошибки на основе контрольных битов и определяет
        позицию ошибочного бита.

        Args:
            data (str): Закодированная двоичная строка

        Returns:
            int or None: Позиция ошибки или None, если ошибок нет
        """
        if self.debug:
            print("\nПоиск ошибки:")

        control_values = HammingEncoder()._compute_control_bits(data)
        syndrome = 0

        if self.debug:
            print("Проверка контрольных битов:")

        for power, expected in control_values.items():
            pos = 2 ** power - 1
            actual = data[pos]
            if self.debug:
                print(f"R{2 ** power} (позиция {pos + 1}): ожидалось {expected}, получено {actual}")

            if actual != str(expected):
                syndrome += 2 ** power

        if syndrome == 0:
            if self.debug:
                print("Синдром = 0 - ошибок нет")
            return None
        else:
            if self.debug:
                print(f"Синдром = {syndrome} (ошибка в позиции {syndrome})")
            return syndrome

    # Исправление ошибки в коде (инверсия бита на найденной позиции)
    def _correct_error(self, data, position):
        """
        Исправляет ошибку в указанной позиции.

        Args:
            data (str): Двоичная строка с ошибкой
            position (int): Позиция ошибочного бита

        Returns:
            str: Исправленная двоичная строка
        """
        if position > len(data):
            return data

        data_list = list(data)
        if self.debug:
            print(f"\nИсправление ошибки в позиции {position}")
            print(f"Было: {data_list[position - 1]}, меняем на {1 - int(data_list[position - 1])}")

        data_list[position - 1] = str(1 - int(data_list[position - 1]))
        return ''.join(data_list)

    # Удаление контрольных битов из восстановленного кода
    def _remove_control_bits(self, data):
        """
        Удаляет контрольные биты из восстановленного кода.

        Args:
            data (str): Двоичная строка с контрольными битами

        Returns:
            str: Исходная двоичная строка без контрольных битов
        """
        result = ""
        if self.debug:
            print("\nУдаление контрольных битов:")

        for i, bit in enumerate(data):
            pos = i + 1
            if not HammingEncoder._is_power_of_two(pos):
                if self.debug:
                    print(f"Сохраняем бит данных D{pos}: {bit}")
                result += bit
            else:
                if self.debug:
                    print(f"Пропускаем контрольный бит R{pos}")

        return result

    def _visualize_block(self, block, title):
        print(f"\n{title}:")
        for i, bit in enumerate(block):
            pos = i + 1
            if HammingEncoder._is_power_of_two(pos):
                print(f"[R{pos}:{bit}]", end=" ")
            else:
                print(f"D{pos}:{bit}", end=" ")
        print()


# Функция для внесения ошибки в код
def introduce_error(data):
    """
    Вносит случайную ошибку в двоичную строку.

    Случайным образом выбирает позицию и инвертирует бит в этой позиции.

    Args:
        data (str): Исходная двоичная строка

    Returns:
        str: Двоичная строка с одной инвертированной ошибкой
    """
    pos = random.randint(0, len(data) - 1)
    corrupted = str(1 - int(data[pos]))  # Инверсия случайного бита
    return data[:pos] + corrupted + data[pos + 1:]


# Разделение бинарной строки на блоки заданного размера
def split_into_blocks(binary_str, block_size=16):
    """
    Разделяет двоичную строку на блоки заданного размера.

    Args:
        binary_str (str): Исходная двоичная строка
        block_size (int): Размер блока (по умолчанию 16 бит)

    Returns:
        list: Список двоичных строк заданного размера
    """
    return [binary_str[i:i + block_size] for i in range(0, len(binary_str), block_size)]


# Преобразование текста в бинарный формат
def convert_text_to_binary(text, chars_per_block=4):
    """
    Преобразует текст в бинарный формат.

    Каждый символ преобразуется в 8-битное двоичное представление.
    Текст разбивается на блоки по заданному количеству символов.

    Args:
        text (str): Исходный текст
        chars_per_block (int): Количество символов в блоке

    Returns:
        list: Список двоичных строк, представляющих блоки текста
    """
    return [''.join(bin(ord(char))[2:].zfill(8) for char in text[i:i + chars_per_block]) for i in
            range(0, len(text), chars_per_block)]


# Основная функция для работы программы
def main():
    """
    Основная функция программы.

    Реализует интерактивный интерфейс для:
    1. Ввода данных (текст или бинарная последовательность)
    2. Кодирования данных с помощью кода Хэмминга
    3. Возможного внесения ошибок
    4. Декодирования данных
    5. Вывода результатов в виде таблицы
    """
    debug = int(input("Включить отладочный вывод? (1 - да, 0 - нет): "))

    mode = int(input("1 - текст, 2 - бинарный ввод: "))
    if mode == 1:
        text = input("Введите текст: ")
        packets = convert_text_to_binary(text)
        if debug:
            print("\nПреобразованные бинарные блоки:")
            for i, block in enumerate(packets):
                print(f"Блок {i + 1}: {block}")
    else:
        binary_data = input("Введите бинарную последовательность: ")
        packets = split_into_blocks(binary_data)
        if debug:
            print("\nРазделенные бинарные блоки:")
            for i, block in enumerate(packets):
                print(f"Блок {i + 1}: {block}")

    add_error = int(input("Добавить ошибку? (1 - да, 0 - нет): "))
    encoder = HammingEncoder(debug=debug)
    encoded_packets = encoder.encode(packets)

    if add_error:
        if debug:
            print("\nВнесение ошибок в закодированные блоки:")
        for packet in encoded_packets:
            packet["corrupted"] = introduce_error(packet["encoded"])
            if debug:
                print(f"Исходный: {packet['encoded']}")
                print(f"С ошибкой: {packet['corrupted']}")

    decoder = HammingDecoder(debug=debug)
    decoded_packets = decoder.decode([p["corrupted"] if "corrupted" in p else p["encoded"] for p in encoded_packets])

    for idx in range(len(encoded_packets)):
        encoded_packets[idx].update(decoded_packets[idx])

    table = PrettyTable()
    table.field_names = encoded_packets[0].keys()
    for row in encoded_packets:
        table.add_row(row.values())
    print("\nИтоговые результаты:")
    print(table)


if __name__ == "__main__":
    main()