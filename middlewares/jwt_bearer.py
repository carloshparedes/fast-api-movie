from fastapi.security import HTTPBearer
from jwt_manager import create_token, validate_token
from fastapi import HTTPException, Request

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        valid_token = validate_token(auth.credentials)
        if valid_token['username'] != 'admin':
            raise HTTPException(status_code=403, detail="Unauthorized")