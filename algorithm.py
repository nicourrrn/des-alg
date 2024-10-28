import constants


def F(right: list, round_key: list) -> list:
    # Розширення 32 бітів до 48
    expanded_right = [right[i - 1] for i in constants.E]
    # XOR із ключем
    xor_with_key = [expanded_right[i] ^ round_key[i] for i in range(48)]

    # Розбиття на 8 блоків по 6 бітів і заміна через S-блоки
    s_output = []
    for i in range(8):
        block = xor_with_key[i * 6 : (i + 1) * 6]
        row = (block[0] << 1) | block[5]
        column = (block[1] << 3) | (block[2] << 2) | (block[3] << 1) | block[4]
        s_value = constants.S_BOX[i][row][column]
        s_output.extend([int(b) for b in f"{s_value:04b}"])

    # Перестановка P
    return [s_output[i - 1] for i in constants.P]


def encrypt(data: bytes, key: bytes) -> bytes:
    if len(data) != 64:
        raise ValueError(f"Data size must be 8 bytes, but got {len(data)} bytes")
    if len(key) != 64:
        raise ValueError(f"Key size must be 8 bytes, but got {len(key)} bytes")

    # Початкова перестановка
    encrypted = [data[i - 1] for i in constants.IP]
    left, right = encrypted[:32], encrypted[32:]

    # Генерація підключів
    round_key = [key[i - 1] for i in constants.PC_1]
    left_key, right_key = round_key[:28], round_key[28:]

    for i in range(16):
        # Циклічний зсув ключа та отримання підключу
        left_key = shift_left(list(left_key), constants.shifts[i])
        right_key = shift_left(list(right_key), constants.shifts[i])
        combined_key = left_key + right_key
        round_key = [combined_key[j - 1] for j in constants.PC_2]

        # Застосування функції F
        new_left = right
        right = [left[k] ^ F(right, round_key)[k] for k in range(32)]
        left = new_left

    # Кінцева перестановка
    encrypted = right + left
    encrypted = [encrypted[i - 1] for i in constants.FP]

    return bytes(encrypted)


def decrypt(data: bytes, key: bytes) -> bytes:
    if len(data) != 64:
        raise ValueError(f"Data size must be 8 bytes, but got {len(data)} bytes")
    if len(key) != 64:
        raise ValueError(f"Key size must be 8 bytes, but got {len(key)} bytes")

    # Початкова перестановка
    decrypted = [data[i - 1] for i in constants.IP]
    left, right = decrypted[:32], decrypted[32:]

    # Генерація підключів
    round_key = [key[i - 1] for i in constants.PC_1]
    left_key, right_key = round_key[:28], round_key[28:]

    # Зберігаємо всі підключі для зворотного порядку
    subkeys = []
    for i in range(16):
        # Циклічний зсув ключа та отримання підключу
        left_key = shift_left(list(left_key), constants.shifts[i])
        right_key = shift_left(list(right_key), constants.shifts[i])
        combined_key = left_key + right_key
        round_key = [combined_key[j - 1] for j in constants.PC_2]
        subkeys.append(round_key)

    # Виконуємо раунди розшифрування з підключами в зворотному порядку
    for i in range(15, -1, -1):
        # Застосування функції F з підключем у зворотному порядку
        new_left = right
        right = [left[k] ^ F(right, subkeys[i])[k] for k in range(32)]
        left = new_left

    # Кінцева перестановка
    decrypted = right + left
    decrypted = [decrypted[i - 1] for i in constants.FP]

    return bytes(decrypted)


def str_to_bytes(data: str) -> bytes:
    result = []
    for i in data.encode():
        result.extend(bin(i)[2:].zfill(8))
    return bytes(map(int, result))


def bytes_to_str(data: list[int]) -> str:
    result = ""
    for i in range(0, len(data), 8):
        result += to_str(data[i : i + 8])
    return result


def to_str(data: list[int]) -> str:
    result = 0
    for i in data:
        result = (result << 1) + i
    return chr(result)


def shift_left(arr: list[int], n: int) -> bytes:
    return bytes(arr[n:] + arr[:n])


if __name__ == "__main__":
    original_data = str_to_bytes("testdata")  # 8 байтів (64 біти)
    key = str_to_bytes("examplek")  # 8 байтів (64 біти)
    if len(original_data) != len(key) != 64:
        raise ValueError(
            f"Data size must be 8 bytes, but got {len(original_data)} bytes"
        )

    # Шифрування
    encrypted_data = encrypt(original_data, key)

    # Розшифрування
    decrypted_data = decrypt(encrypted_data, key)

    assert (
        decrypted_data == original_data
    ), "Розшифрування не відновлює оригінальні дані!"

    print(
        f"Успішно! Оригінальні дані: {bytes_to_str(list(original_data))} == {bytes_to_str(list(decrypted_data))}"
    )
