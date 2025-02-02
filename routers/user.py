from fastapi import APIRouter
from jwt_manager import create_token
from fastapi.responses import JSONResponse 
from services.schemas.user import User

user_router = APIRouter()

@user_router.post("/login", tags=["auth"])
def login(user: User):
     if user.username == "admin" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content={"token": token})
    