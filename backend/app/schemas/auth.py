import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class RegisterRequest(BaseModel):
    email: str
    password: str = Field(
        ...,
        min_length=6,
        description="Password must be at least 6 characters",
    )
    name: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, value: str) -> str:
        value = value.strip().lower()
        if not EMAIL_REGEX.match(value):
            raise ValueError("Invalid email format.")
        return value

class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, value: str) -> str:
        value = value.strip().lower()
        if not EMAIL_REGEX.match(value):
            raise ValueError("Invalid email format.")
        return value
