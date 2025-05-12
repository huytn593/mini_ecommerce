from fastapi import APIRouter, Depends, Body
from ..models.user import UserCreate, UserLogin
from ..controllers import auth
from ..utils.auth import verify_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserCreate = Body(...)):
    return await auth.register_user(user)

@router.post("/login")
async def login(user: UserLogin = Body(...)):
    return await auth.login_user(user)

@router.get("/me")
async def get_current_user(payload: dict = Depends(verify_token)):
    return await auth.get_current_user(payload["sub"])
