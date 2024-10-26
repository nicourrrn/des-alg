from icecream import ic

import constants


def encrypt(data: bytes, key: bytes) -> bytes:
    if len(data) != 64:
        raise ValueError(f"Data size must be 64 bytes, but get {len(data)} bytes")
    if len(key) != 64:
        raise ValueError(f"Key size must be 64 bytes, but get {len(key)} bytes")

    encrypted = [data[i - 1] for i in constants.IP]
    left, right = encrypted[:32], encrypted[32:]

    round_key = [key[i - 1] for i in constants.PC_1]
    left_key, right_key = round_key[:28], round_key[28:]

    for i in range(16):
        left_key = shift_left(list(left_key), constants.shifts[i])
        right_key = shift_left(list(right_key), constants.shifts[i])

        combined_key = left_key + right_key
        round_key = [combined_key[i - 1] for i in constants.PC_2]
        # TODO change to F function
        left, right = right, [left[i] ^ right[i] for i in range(32)]

    encrypted = right + left
    encrypted = [encrypted[i - 1] for i in constants.FP]

    return bytes(encrypted)


def decrypt(data: bytes, key: bytes) -> bytes:
    if len(data) != 64:
        raise ValueError(f"Data size must be 64 bytes, but get {len(data)} bytes")
    if len(key) != 64:
        raise ValueError(f"Key size must be 64 bytes, but get {len(key)} bytes")

    encrypted = [data[i - 1] for i in constants.IP]
    left, right = encrypted[:32], encrypted[32:]

    round_key = [key[i - 1] for i in constants.PC_1]
    left_key, right_key = round_key[:28], round_key[28:]

    for i in range(15, -1, -1):
        left_key = shift_left(list(left_key), constants.shifts[i])
        right_key = shift_left(list(right_key), constants.shifts[i])

        combined_key = left_key + right_key
        round_key = [combined_key[i - 1] for i in constants.PC_2]

        # TODO change to F function
        left, right = right, [left[i] ^ right[i] for i in range(32)]

    encrypted = right + left
    encrypted = [encrypted[i - 1] for i in constants.FP]

    return bytes(encrypted)


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
    data = "12345678"
    key = "87654321"
    data = str_to_bytes(data)
    key = str_to_bytes(key)

    encresult = list(encrypt(data, key))
    decresult = decrypt(bytes(encresult), key)
    print(f"{list(data)}\n{list(decresult)}")
    print(f"Encrypted data: {bytes_to_str(encresult)}")
