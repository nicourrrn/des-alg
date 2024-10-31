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
    #    import uvicorn
    #    uvicorn.run(app, host="0.0.0.0", port=8000)
    from ctypes import *

    libc = CDLL("./lib.so")
    print(libc.decrypt(libc.encrypt("hello", "world"), "world"))
