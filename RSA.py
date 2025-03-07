import random


class RSA:
    def __init__(self, key_size=25):
        """
        Инициализация RSA с генерацией ключей.
        key_size - размер простых чисел в битах.
        """
        self.key_size = key_size
        self.e, self.d, self.n = self._generate_keys()

    def _power(self, base, expo, m):
        """
        Быстрое возведение в степень по модулю.
        """
        res = 1
        base = base % m
        while expo > 0:
            if expo & 1:
                res = (res * base) % m
            base = (base * base) % m
            expo //= 2
        return res

    def _gcd(self, a, b):
        """
        Нахождение наибольшего общего делителя (НОД).
        """
        return a if b == 0 else self._gcd(b, a % b)

    def _mod_inverse(self, e, phi):
        """
        Нахождение обратного элемента по модулю phi.
        """

        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            g, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return g, x, y

        g, x, _ = extended_gcd(e, phi)
        if g != 1:
            raise ValueError("Обратного элемента не существует")
        return x % phi

    def _is_prime(self, n):
        """
        Проверка числа на простоту.
        """
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def _generate_large_prime(self):
        """
        Генерация случайного простого числа заданной длины.
        """
        while True:
            num = random.getrandbits(self.key_size) | (1 << self.key_size - 1) | 1
            if self._is_prime(num):
                return num

    def _find_largest_coprime(self, phi):
        """
        Поиск наибольшего числа, взаимно простого с phi.
        """
        for e in range(phi - 2, 1, -1):
            if self._gcd(e, phi) == 1:
                return e
        return -1

    def _generate_keys(self):
        """
        Генерация ключей RSA.
        """
        p = self._generate_large_prime()
        q = self._generate_large_prime()
        n = p * q
        phi = (p - 1) * (q - 1)
        e = self._find_largest_coprime(phi)
        d = self._mod_inverse(e, phi)
        return e, d, n

    def encrypt(self, message):
        """
        Шифрование строки message.
        """
        return [self._power(m, self.e, self.n) for m in message.encode('utf-8')]

    def decrypt(self, encrypted):
        """
        Дешифрование списка зашифрованных символов.
        """
        decrypted = [self._power(c, self.d, self.n) for c in encrypted]
        try:
            return bytes(decrypted).decode('utf-8')
        except UnicodeDecodeError:
            return "Ошибка при декодировании сообщения"

    def get_public_key(self):
        """
        Возвращает публичный ключ (e, n).
        """
        return self.e, self.n

    def get_private_key(self):
        """
        Возвращает приватный ключ (d, n).
        """
        return self.d, self.n


# Основной код для демонстрации работы
if __name__ == "__main__":
    rsa = RSA()
    print(f"Публичный ключ (e, n): {rsa.get_public_key()}")
    print(f"Приватный ключ (d, n): {rsa.get_private_key()}")

    message = "if 14 - wr fso "
    print(f"Оригинальное сообщение: {message}")

    encrypted_message = rsa.encrypt(message)
    print(f"Закодированное сообщение: {encrypted_message}")

    decrypted_message = rsa.decrypt(encrypted_message)
    print(f"Декодированное сообщение: {decrypted_message}")