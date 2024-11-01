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


async def is_key_weak(key: str) -> bool:
    return False


@app.post("/check_key")
async def check_key(key: str):
    return {"is_weak": await is_key_weak(key)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
