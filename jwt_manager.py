from jwt import encode

def create_token(data: dict):
    return encode(payload=data, key="secret", algorithm="HS256")