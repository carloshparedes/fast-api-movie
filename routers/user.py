from fastapi import APIRouter
from pydantic import BaseModel
from jwt_manager import create_token
from fastapi.responses import JSONResponse 

user_router = APIRouter()

class User(BaseModel):
    username: str
    password: str

@user_router.post("/login", tags=["auth"])
def login(user: User):
     if user.username == "admin" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content={"token": token})
    