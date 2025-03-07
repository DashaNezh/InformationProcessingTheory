import numpy as np
import random
from prettytable import PrettyTable

# Класс для кодирования данных по коду Хэмминга
class HammingEncoder:
    def __init__(self):
        self.encoded_data = []

    # Кодирование списка двоичных блоков
    def encode(self, data_blocks):
        for block in data_blocks:
            extended_block = self._insert_control_bits(block)  # Добавление контрольных битов
            control_values = self._compute_control_bits(extended_block)  # Вычисление значений контрольных битов
            final_code = self._apply_control_bits(extended_block, control_values)  # Установка контрольных битов в код
            self.encoded_data.append({"original": block, "encoded": final_code})
        return self.encoded_data

    # Метод вычисления значений контрольных битов
    def _compute_control_bits(self, data):
        control_values = {}
        for idx, bit in enumerate(data):
            bit_position = bin(idx + 1)[2:][::-1]  # Представление индекса в двоичной системе (в обратном порядке)
            for i, bit_value in enumerate(bit_position):
                if bit_value == '1':
                    control_values[i] = control_values.get(i, 0) + int(bit)
        return {k: v % 2 for k, v in control_values.items()}  # Вычисляем четность битов

    # Метод установки контрольных битов в соответствующие позиции
    def _apply_control_bits(self, data, control_values):
        data_list = list(data)
        for pos, value in control_values.items():
            data_list[2 ** pos - 1] = str(value)
        return ''.join(data_list)

    # Добавление контрольных битов в код
    def _insert_control_bits(self, data):
        result = ""
        index = 1
        while data:
            if self._is_power_of_two(index):  # Если позиция - степень двойки, добавляем контрольный бит
                result += "0"
            else:
                result += data[0]
                data = data[1:]
            index += 1
        return result

    @staticmethod
    def _is_power_of_two(n):
        return (np.log2(n) % 1) == 0  # Проверка, является ли число степенью двойки


# Класс для декодирования данных по коду Хэмминга
class HammingDecoder:
    def __init__(self):
        self.decoded_data = []

    # Декодирование списка двоичных блоков
    def decode(self, encoded_blocks):
        for block in encoded_blocks:
            error_position = self._find_error(block)  # Определение позиции ошибки
            if error_position:
                block = self._correct_error(block, error_position)  # Исправление ошибки
            self.decoded_data.append({"corrected": block, "decoded": self._remove_control_bits(block)})
        return self.decoded_data

    # Поиск ошибки на основе контрольных битов
    def _find_error(self, data):
        control_values = HammingEncoder()._compute_control_bits(data)
        error_position = sum(2 ** idx for idx, bit in control_values.items() if data[2 ** idx - 1] != str(bit))
        return error_position if error_position else None

    # Исправление ошибки в коде (инверсия бита на найденной позиции)
    def _correct_error(self, data, position):
        data_list = list(data)
        data_list[position - 1] = str(1 - int(data_list[position - 1]))
        return ''.join(data_list)

    # Удаление контрольных битов из восстановленного кода
    def _remove_control_bits(self, data):
        result = ""
        index = 1
        while data:
            if not HammingEncoder._is_power_of_two(index):  # Пропускаем контрольные биты
                result += data[0]
            data = data[1:]
            index += 1
        return result


# Функция для внесения ошибки в код
def introduce_error(data):
    pos = random.randint(0, len(data) - 1)
    corrupted = str(1 - int(data[pos]))  # Инверсия случайного бита
    return data[:pos] + corrupted + data[pos + 1:]


# Разделение бинарной строки на блоки заданного размера
def split_into_blocks(binary_str, block_size=16):
    return [binary_str[i:i + block_size] for i in range(0, len(binary_str), block_size)]


# Преобразование текста в бинарный формат
def convert_text_to_binary(text, chars_per_block=4):
    return [''.join(bin(ord(char))[2:].zfill(8) for char in text[i:i + chars_per_block]) for i in range(0, len(text), chars_per_block)]


# Основная функция для работы программы
def main():
    mode = int(input("1 - текст, 2 - бинарный ввод: "))
    if mode == 1:
        text = input("Введите текст: ")
        packets = convert_text_to_binary(text)
    else:
        binary_data = input("Введите бинарную последовательность: ")
        packets = split_into_blocks(binary_data)

    add_error = int(input("Добавить ошибку? (1 - да, 0 - нет): "))
    encoder = HammingEncoder()
    encoded_packets = encoder.encode(packets)

    if add_error:
        for packet in encoded_packets:
            packet["corrupted"] = introduce_error(packet["encoded"])

    decoder = HammingDecoder()
    decoded_packets = decoder.decode([p["corrupted"] if "corrupted" in p else p["encoded"] for p in encoded_packets])

    for idx in range(len(encoded_packets)):
        encoded_packets[idx].update(decoded_packets[idx])

    table = PrettyTable()
    table.field_names = encoded_packets[0].keys()
    for row in encoded_packets:
        table.add_row(row.values())
    print(table)


if __name__ == "__main__":
    main()
