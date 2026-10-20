from fastapi import APIRouter, Depends, status

from auth.dependencies import get_current_user
from schemas.auth import LoginRequest, RegisterRequest
from services.user_service import (
    get_user_request,
    login_user_request,
    register_user_request,
)

user_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest):
    return register_user_request(
        email=request.email,
        password=request.password,
        name=request.name,
    )

@user_router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginRequest):
    return login_user_request(
        email=request.email,
        password=request.password,
    )

@user_router.get("/me", status_code=status.HTTP_200_OK)
def get_me(current_user: dict = Depends(get_current_user)):
    return get_user_request(current_user)
