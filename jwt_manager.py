from jwt import encode
from jwt import decode

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="secret", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    decoded_token: dict = decode(token, key="secret", algorithms=["HS256"])
    return decoded_token 