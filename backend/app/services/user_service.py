from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status
from auth.security import create_access_token, hash_password, verify_password
from db.user_queries import create_user, get_user_by_email, get_user_by_id

def register_user_request(
    email: str,
    password: str,
    name: Optional[str] = None,
):
    normalized_email = email.strip().lower()
    if get_user_by_email(normalized_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists.",
        )

    new_user_id = create_user(
        email=normalized_email,
        password_hash=hash_password(password),
        name=name,
    )
    token = create_access_token(user_id=new_user_id, email=normalized_email)
    expires_at = (
        datetime.now(timezone.utc) + timedelta(hours=24)
    ).isoformat()

    return {
        "success": True,
        "message": "User registered successfully.",
        "data": {
            "token": token,
            "user": {
                "id": new_user_id,
                "name": name.strip() if name and name.strip() else normalized_email.split("@")[0],
                "email": normalized_email,
            },
            "expiresAt": expires_at,
        },
    }

def login_user_request(email: str, password: str):
    normalized_email = email.strip().lower()
    user = get_user_by_email(normalized_email)
    if not user or not verify_password(password, user.get("password") or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user_id=user["id"], email=user["email"])
    expires_at = (
        datetime.now(timezone.utc) + timedelta(hours=24)
    ).isoformat()
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


def get_user_request(current_user: dict):
    user = get_user_by_id(int(current_user["user_id"]))
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
