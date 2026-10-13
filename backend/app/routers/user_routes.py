import re
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field, field_validator
from db.user_queries import get_user_by_email, get_user_by_id, create_user
from utils.auth import hash_password, verify_password, create_access_token, get_current_user

user_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class RegisterRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    name: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        v = v.strip().lower()
        if not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format.")
        return v

class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        v = v.strip().lower()
        if not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format.")
        return v

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest):
    normalized_email = request.email.strip().lower()

    # 1. Check for duplicate email
    existing_user = get_user_by_email(normalized_email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists.",
        )

    # 2. Hash password securely
    hashed_pwd = hash_password(request.password)

    # 3. Store user in database
    new_user_id = create_user(
        email=normalized_email,
        password_hash=hashed_pwd,
        name=request.name,
    )

    token = create_access_token(user_id=new_user_id, email=normalized_email)
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()

    return {
        "success": True,
        "message": "User registered successfully.",
        "data": {
            "token": token,
            "user": {
                "id": new_user_id,
                "name": request.name.strip() if request.name and request.name.strip() else normalized_email.split("@")[0],
                "email": normalized_email,
            },
            "expiresAt": expires_at
        },
    }

@user_router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginRequest):
    normalized_email = request.email.strip().lower()

    # 1. Retrieve user by email
    user = get_user_by_email(normalized_email)

    # 2. Verify password with stored hash
    if not user or not verify_password(request.password, user.get("password") or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Generate signed 24h JWT
    token = create_access_token(user_id=user["id"], email=user["email"])
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()

    return {
        "success": True,
        "message": "Login successful.",
        "data": {
            "token": token,
            "user": {
                "id": user["id"],
                "name": user.get("name") or user["email"].split("@")[0],
                "email": user["email"],
            },
            "expiresAt": expires_at,
        },
    }

@user_router.get("/me", status_code=status.HTTP_200_OK)
def get_me(current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return {
        "success": True,
        "message": "User profile loaded successfully.",
        "data": user,
    }
