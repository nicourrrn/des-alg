import des
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/encrypt")
async def encrypt(key: str, message: str):
    print(f"Encrypting message, {key=}, {message=}")


@app.post("/decrypt")
async def decrypt(req: Request):
    data = await req.json()
    key = data["key"]
    message = data["message"]


async def is_key_weak(key: str) -> bool:
    return False


@app.post("/check_key")
async def check_key(key: str):
    return {"is_weak": await is_key_weak(key)}


if __name__ == "__main__":
    result = des.encrypt(0x12123123, 0x12345)
    print(result)
