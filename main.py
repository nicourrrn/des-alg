from fastapi import FastAPI

app = FastAPI()


@app.post("/encrypt")
async def encrypt():
    return {"message": "Encrypting message"}


@app.post("/decrypt")
async def decrypt():
    return {"message": "Decrypting message"}


async def is_key_weak(key: str) -> bool:
    return False


@app.post("/check_key")
async def check_key(key: str):
    return {"is_weak": await is_key_weak(key)}
