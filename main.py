import des
from fastapi import FastAPI, Request

app = FastAPI()

# case1
# Convert a string to 64-bit format by padding or truncating it.
def to_64_bit(input_str: str) -> int:
    # Ensure the string is exactly 8 characters (64 bits)
    input_str = input_str.ljust(8)[:8]
    # Convert to bytes and then to an integer
    return int.from_bytes(input_str.encode(), 'big')


# case2
# Розбиває рядок на блоки по 8 байт (64 біти)
def split_to_64_bit_blocks(input_str: str):
    # Розбиває рядок на блоки по 8 байт (64 біти)
    blocks = [input_str[i:i + 8] for i in range(0, len(input_str), 8)]
    # Перетворює кожен блок у 64-бітове ціле число
    return [int.from_bytes(block.ljust(8).encode(), 'big') for block in blocks]

# big or little 



@app.post("/encrypt")
async def encrypt(key: str, message: str):
    print(f"Encrypting message, {key=}, {message=}")


@app.post("/decrypt")
async def decrypt(req: Request):
    data = await req.json()
    key = data["key"]
    message = data["message"]
    
    key_64bit = to_64_bit(key)
    message_64bit = to_64_bit(message)
    return {"decrypted": des.decrypt(message_64bit, key_64bit)}

async def is_key_weak(key: str) -> bool:
    return False


@app.post("/check_key")
async def check_key(key: str):
    return {"is_weak": await is_key_weak(key)}


if __name__ == "__main__":
    result = des.encrypt(0x12123123, 0x12345)
    print(result)
