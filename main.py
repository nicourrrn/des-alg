import math
import string

import des
from fastapi import FastAPI, Request

app = FastAPI()


# case1
# Convert a string to 64-bit format by padding or truncating it.
def to_64_bit(input_str: str) -> int:
    # Ensure the string is exactly 8 characters (64 bits)
    input_str = input_str.ljust(8)[:8]
    # Convert to bytes and then to an integer
    return int.from_bytes(input_str.encode(), "big")


# case2
# Розбиває рядок на блоки по 8 байт (64 біти)
def split_to_64_bit_blocks(input_str: str):
    # Розбиває рядок на блоки по 8 байт (64 біти)
    blocks = [input_str[i : i + 8] for i in range(0, len(input_str), 8)]
    # Перетворює кожен блок у 64-бітове ціле число
    return [int.from_bytes(block.ljust(8).encode(), "big") for block in blocks]


# big or little


@app.post("/encrypt")
async def encrypt(key: str, message: str):
    keys = split_to_64_bit_blocks(key)
    filan_message = ""
    for i, data in enumerate(split_to_64_bit_blocks(message)):
        result = des.des_encrypt(data, keys[i % len(keys)])
        filan_message += f"{result:016x}"
    print(f"Result is :{filan_message}")
    return {"result": filan_message}


@app.post("/decrypt")
async def decrypt(req: Request):
    data = await req.json()
    key = data["key"]
    message = data["message"]

    keys = split_to_64_bit_blocks(key)
    filan_message = ""
    for i, data in enumerate(
        [int(f"0x{message[i:i+16]}", 16) for i in range(0, len(message), 16)]
    ):
        result = des.des_decrypt(data, keys[i % len(keys)])
        filan_message += result.to_bytes(8, "big").decode()
    print(f"Result is :{filan_message}")
    return {"result": filan_message}


def calculate_entropy(key):
    """Обчислює ентропію ключа."""
    charset_size = 0
    if any(c in string.ascii_lowercase for c in key):
        charset_size += 26  # малі літери
    if any(c in string.ascii_uppercase for c in key):
        charset_size += 26  # великі літери
    if any(c in string.digits for c in key):
        charset_size += 10  # цифри
    if any(c in string.punctuation for c in key):
        charset_size += len(string.punctuation)  # спеціальні символи

    if charset_size == 0:
        return 0

    entropy = len(key) * math.log2(charset_size)
    return entropy


def check_key_strength(key):
    length = len(key)
    entropy = calculate_entropy(key)
    has_upper = any(c.isupper() for c in key)
    has_lower = any(c.islower() for c in key)
    has_digit = any(c.isdigit() for c in key)
    has_special = any(c in string.punctuation for c in key)

    # Оцінка стійкості на основі довжини та різноманітності символів
    if length < 8 or entropy < 40:
        return "Низька стійкість"
    elif (
        length >= 8
        and entropy >= 40
        and (has_upper + has_lower + has_digit + has_special) >= 3
    ):
        return "Середня стійкість"
    elif (
        length >= 12
        and entropy >= 60
        and all([has_upper, has_lower, has_digit, has_special])
    ):
        return "Висока стійкість"
    else:
        return "Середня стійкість"


@app.get("/strench")
async def is_key_weak(key: str):
    strength = check_key_strength(key)
    entropy = calculate_entropy(key)
    return {"result": strength, "entropy": entropy}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
