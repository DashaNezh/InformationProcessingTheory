import random


class RSA:
    def __init__(self, key_size=25):
        """
        Инициализация объекта RSA с генерацией ключей.
        
        Args:
            key_size (int): Размер простых чисел в битах, используемых для генерации ключей.
                           По умолчанию равен 25 битам.
        
        Attributes:
            key_size (int): Размер ключа в битах
            e (int): Публичная экспонента (часть публичного ключа)
            d (int): Приватная экспонента (часть приватного ключа)
            n (int): Модуль (общая часть для публичного и приватного ключей)
        """
        self.key_size = key_size
        self.e, self.d, self.n = self._generate_keys()

    def _power(self, base, expo, m):
        """
        Быстрое возведение в степень по модулю (метод быстрого возведения в степень).
        
        Args:
            base (int): Основание степени
            expo (int): Показатель степени
            m (int): Модуль
            
        Returns:
            int: Результат вычисления (base^expo) mod m
            
        Note:
            Использует алгоритм быстрого возведения в степень для эффективного
            вычисления больших степеней по модулю.
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
        Нахождение наибольшего общего делителя (НОД) двух чисел.
        
        Args:
            a (int): Первое число
            b (int): Второе число
            
        Returns:
            int: Наибольший общий делитель чисел a и b
            
        Note:
            Использует алгоритм Евклида для нахождения НОД.
        """
        return a if b == 0 else self._gcd(b, a % b)

    def _mod_inverse(self, e, phi):
        """
        Нахождение обратного элемента по модулю phi.
        
        Args:
            e (int): Число, для которого ищется обратный элемент
            phi (int): Модуль (функция Эйлера)
            
        Returns:
            int: Обратный элемент к e по модулю phi
            
        Raises:
            ValueError: Если обратный элемент не существует
            
        Note:
            Использует расширенный алгоритм Евклида для нахождения
            обратного элемента.
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
        
        Args:
            n (int): Число для проверки
            
        Returns:
            bool: True, если число простое, False в противном случае
            
        Note:
            Использует оптимизированный алгоритм проверки на простоту,
            проверяя делители до квадратного корня из n.
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
        
        Returns:
            int: Случайное простое число размером key_size бит
            
        Note:
            Генерирует случайные числа и проверяет их на простоту
            до тех пор, пока не будет найдено простое число.
        """
        while True:
            num = random.getrandbits(self.key_size) | (1 << self.key_size - 1) | 1
            if self._is_prime(num):
                return num

    def _find_largest_coprime(self, phi):
        """
        Поиск наибольшего числа, взаимно простого с phi.
        
        Args:
            phi (int): Значение функции Эйлера
            
        Returns:
            int: Наибольшее число, взаимно простое с phi
            
        Note:
            Используется для выбора публичной экспоненты e.
            Начинает поиск с phi-2 и двигается вниз.
        """
        for e in range(phi - 2, 1, -1):
            if self._gcd(e, phi) == 1:
                return e
        return -1

    def _generate_keys(self):
        """
        Генерация ключей RSA.
        
        Returns:
            tuple: (e, d, n), где:
                - e: публичная экспонента
                - d: приватная экспонента
                - n: модуль
                
        Note:
            Генерирует два простых числа p и q, вычисляет n = p*q,
            функцию Эйлера phi = (p-1)*(q-1), выбирает e и вычисляет d.
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
        Шифрование сообщения с использованием публичного ключа.
        
        Args:
            message (str): Сообщение для шифрования
            
        Returns:
            list: Список зашифрованных чисел
            
        Note:
            Каждый символ сообщения преобразуется в его ASCII-код,
            затем шифруется с помощью публичного ключа (e, n).
        """
        return [self._power(m, self.e, self.n) for m in message.encode('utf-8')]

    def decrypt(self, encrypted):
        """
        Дешифрование сообщения с использованием приватного ключа.
        
        Args:
            encrypted (list): Список зашифрованных чисел
            
        Returns:
            str: Расшифрованное сообщение
            
        Note:
            Каждое зашифрованное число расшифровывается с помощью
            приватного ключа (d, n) и преобразуется обратно в символ.
        """
        decrypted = [self._power(c, self.d, self.n) for c in encrypted]
        try:
            return bytes(decrypted).decode('utf-8')
        except UnicodeDecodeError:
            return "Ошибка при декодировании сообщения"

    def get_public_key(self):
        """
        Получение публичного ключа.
        
        Returns:
            tuple: (e, n) - публичная экспонента и модуль
        """
        return self.e, self.n

    def get_private_key(self):
        """
        Получение приватного ключа.
        
        Returns:
            tuple: (d, n) - приватная экспонента и модуль
        """
        return self.d, self.n


# Основной код для демонстрации работы
if __name__ == "__main__":
    rsa = RSA()
    print(f"Публичный ключ (e, n): {rsa.get_public_key()}")
    print(f"Приватный ключ (d, n): {rsa.get_private_key()}")

    message = "this is a secret message. do not distribute it!"
    print(f"Оригинальное сообщение: {message}")

    encrypted_message = rsa.encrypt(message)
    print(f"Закодированное сообщение: {encrypted_message}")

    decrypted_message = rsa.decrypt(encrypted_message)
    print(f"Декодированное сообщение: {decrypted_message}")