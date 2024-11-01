from fastapi import FastAPI, Request

from algorithm import bytes_to_str
from algorithm import decrypt as dec
from algorithm import encrypt as enc
from algorithm import str_to_bytes

app = FastAPI()


@app.post("/encrypt")
async def encrypt(key: str, message: str):
    print(f"Encrypting message, {key=}, {message=}")
    encrypted = enc(str_to_bytes(key), str_to_bytes(message))
    print(f"Encrypted message: {encrypted}")
    return {"message": bytes_to_str(list(encrypted))}


@app.post("/decrypt")
async def decrypt(req: Request):
    data = await req.json()
    key = data["key"]
    message = data["message"]
    print(f"Decrypting message, {key=}, {message=}")
    decrypted = dec(str_to_bytes(key), str_to_bytes(message))
    print(f"Decrypted message: {decrypted}")
    return {"message": bytes_to_str(list(decrypted))}


async def is_key_weak(key: str) -> bool:
    return False


@app.post("/check_key")
async def check_key(key: str):
    return {"is_weak": await is_key_weak(key)}


if __name__ == "__main__":
    from ctypes import CDLL, c_uint64

    libc = CDLL("./lib.so")
    result: c_uint64 = libc.encrypt(0x0123456789ABCDEF, 0x133457799BBCDFF1)
    enc_result: c_uint64 = libc.decrypt(result, 0x133457799BBCDFF1)
    print(f"result: {result:0x}, enc_result: {enc_result:0x}")
