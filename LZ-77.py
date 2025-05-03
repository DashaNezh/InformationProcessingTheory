class LZ77:
    def __init__(self, window_size=64):
        self.window_size = window_size

    def find_longest_match(self, search_window, lookahead_buffer):
        best_offset = 0
        max_length = 0
        for i in range(len(search_window) - 1, -1, -1):
            length = 0
            while (length < len(lookahead_buffer) and
                   i + length < len(search_window) and
                   search_window[i + length] == lookahead_buffer[length]):
                length += 1
            if length > max_length:
                max_length = length
                best_offset = len(search_window) - i - 1
                if max_length == len(lookahead_buffer):
                    break
        return best_offset, max_length

    def encode(self, input_string):
        encoded_data = []
        search_window = ""
        lookahead_buffer = input_string
        pos = 0
        while pos < len(input_string):
            if len(search_window) > self.window_size:
                search_window = search_window[-self.window_size:]
            current_char = lookahead_buffer[0]
            offset, length = self.find_longest_match(search_window, lookahead_buffer)
            if length == 0:
                encoded_data.append((current_char, 0, 0, 0, f"0bin({current_char})"))
                search_window += current_char
                lookahead_buffer = lookahead_buffer[1:]
                pos += 1
            else:
                matched_sequence = lookahead_buffer[:length]
                encoded_data.append((
                    matched_sequence,
                    1,
                    offset,
                    length,
                    f"1 {offset} {length}"
                ))
                search_window += matched_sequence
                lookahead_buffer = lookahead_buffer[length:]
                pos += length
        return encoded_data

    def print_encoded_data(self, encoded_data):
        from math import log2, ceil

        def unar(n):
            return '1' * (n - 1) + '0'

        def bin_str(n):
            return bin(n)[3:]

        def mon(i):
            return unar(len(bin_str(i)) + 1) + bin_str(i)

        print(
            "| ШАГ  | ФЛАГ | ПОСЛЕДОВАТЕЛЬНОСТЬ БУКВ | РАССТОЯНИЕ (d) | ДЛИНА (l) | КОДОВАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ | БИТЫ  |")
        print("-" * 107)

        total_len = sum(len(seq) if flag else 1 for seq, flag, *_ in encoded_data)
        lookahead_remaining = total_len
        total_bits = 0

        for i, (sequence, flag, distance, length, code) in enumerate(encoded_data):
            if flag == 0:
                bits = 1 + 8
                code_str = f"0bin({sequence})"
                step_len = 1
            else:
                real_window = max(1, min(total_len - lookahead_remaining, self.window_size))
                offset_bits = max(1, ceil(log2(real_window + 1)))
                offset_bin = format(distance, f'0{offset_bits}b')
                if length == 1:
                    length_bin = '0'
                else:
                    length_bin = mon(length)
                length_bits = len(length_bin)
                code_str = f"1 {offset_bin} {length_bin}"
                bits = 1 + offset_bits + length_bits
                step_len = length
            total_bits += bits
            print(f"| {i:<4} | {flag:<4} | {sequence:<24}| {distance:<14} | {length:<8} | {code_str:<27}| {bits:<5} |")
            lookahead_remaining -= step_len

        print("-" * 107)
        print(f"{'Итого:':>95} {total_bits} бит")


# Пример использования
if __name__ == "__main__":
    input_text = "IF_WE_CANNOT_DO_AS_WE_WOULD_WE_SHOULD_DO_AS_WE_CAN"
    #input_text = "EARLY_TO_BED_AND_EARLY_TO_RISE_MAKES_A_MAN_WISE"
    lz77 = LZ77(window_size=64)
    encoded = lz77.encode(input_text)
    lz77.print_encoded_data(encoded)


