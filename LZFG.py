import math


def ceil_log2(x):
    # Вычисляет верхнюю границу двоичного логарифма числа
    return math.ceil(math.log2(x)) if x > 0 else 1


class SlidingWindow:
    """Класс, представляющий скользящее окно для поиска совпадений"""
    def __init__(self, text):
        self.text = text

    def get_substring(self, pos, length):
        return self.text[pos:pos + length]


class MatchFinder:
    """Класс, выполняющий поиск наилучших совпадений в окне"""
    def __init__(self, window):
        self.window = window

    def find_best_match(self, pos, max_len=17):
        """Ищет наибольшее совпадение строки начиная с позиции pos"""
        best_length = 0
        best_index = None
        for i in range(0, pos):
            length = 0
            while length < max_len and pos + length < len(self.window.text) and self.window.text[i + length] == self.window.text[pos + length]:
                length += 1
            if length > best_length:
                best_length = length
                best_index = i
        return best_length, best_index

    def can_find_pointer_at(self, pos, window_end, max_len=17):
        """Проверяет, возможно ли ссылочное кодирование с данной позиции"""
        if pos >= len(self.window.text):
            return False
        best_length, _ = self.find_best_match(pos, max_len)
        return best_length >= 3

    def choose_literal_length(self, pos, max_literal=16):
        """Определяет длину блока литералов перед переходом на ссылочное кодирование"""
        L = 1
        while L < max_literal and pos + L < len(self.window.text):
            if self.can_find_pointer_at(pos + L, pos + L):
                break
            L += 1
        return L


class CompressionStep:
    """Класс, представляющий один шаг кодирования"""
    def __init__(self, step, match_length, distance, literal_count, code, transmitted, cost, window):
        self.step = step
        self.match_length = match_length
        self.distance = distance
        self.literal_count = literal_count
        self.code = code
        self.transmitted = transmitted
        self.cost = cost
        self.window = window

    def __str__(self):
        dist_field = f"{self.distance[0]}({self.distance[1]})" if self.match_length >= 3 else "-"
        literal_count = "-" if self.match_length >= 3 else self.literal_count
        return f"{self.step:<4} {self.match_length:<14} {dist_field:<18} {literal_count:<14} {self.code:<25} {self.transmitted:<20} {self.cost:<15}"


class LZFGCompressor:
    """Основной класс, выполняющий сжатие текста алгоритмом LZFG"""
    def __init__(self, text):
        self.window = SlidingWindow(text)
        self.finder = MatchFinder(self.window)
        self.text = text
        self.steps = []
        self.total_cost = 0

    def compress(self):
        """Основной метод сжатия текста"""
        pos = 0
        step = 1
        while pos < len(self.text):
            if pos < 3:
                # Кодирование первых символов как литералов
                L = min(16, len(self.text) - pos)
                literal_block = self.text[pos:pos + L]
                code = "0000 " + format(L - 1, '04b') + " bin(" + literal_block + ")"
                cost = 8 + 8 * L
                self.steps.append(CompressionStep(step, 0, None, L, code, literal_block, cost, pos))
                pos += L
                self.total_cost += cost
                step += 1
                continue

            best_length, best_index = self.finder.find_best_match(pos)
            if best_length >= 3:
                # Кодирование ссылки на предыдущее вхождение
                length_code = format(best_length - 2, '04b')
                actual_distance = pos - best_index
                stored_distance = actual_distance - 1
                dist_bits = ceil_log2(pos)
                distance_code = format(stored_distance, '0{}b'.format(dist_bits))
                code = length_code + " " + distance_code
                cost = 4 + dist_bits
                token = self.text[pos:pos + best_length]
                self.steps.append(CompressionStep(step, best_length, (stored_distance, pos), None, code, token, cost, pos))
                pos += best_length
                self.total_cost += cost
                step += 1
            else:
                # Если совпадений нет, кодируем как литералы
                L = self.finder.choose_literal_length(pos)
                literal_block = self.text[pos:pos + L]
                code = "0000 " + format(L - 1, '04b') + " bin(" + literal_block + ")"
                cost = 8 + 8 * L
                self.steps.append(CompressionStep(step, 0, None, L, code, literal_block, cost, pos))
                pos += L
                self.total_cost += cost
                step += 1

    def print_table(self):
        """Выводит таблицу с результатами сжатия"""
        header = f"{'Шаг':<4} {'Длина совп.':<14} {'Расст. до обр.':<18} {'Число букв':<14} {'Кодовые символы':<25} {'Перед. буквы':<20} {'Затраты (бит)':<15}"
        print(header)
        print("-" * len(header))
        for step in self.steps:
            print(step)
        print("-" * len(header))
        print(f"{'Итого':<81} {self.total_cost}")


if __name__ == "__main__":
    text = "early_to_bed_and_early_to_rise_makes_a_man_wise"
    compressor = LZFGCompressor(text)
    compressor.compress()
    compressor.print_table()