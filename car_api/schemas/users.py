from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def username_min_lenght(cls, value):
        if len(value) < 3:
            raise ValueError('Username must be at least 3 characters long')

        return value

    @field_validator('password')
    def password_min_lenght(cls, value):
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')

        return value


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator('username')
    def username_min_lenght(cls, value):
        if len(value) < 3:
            raise ValueError('Username must be at least 3 characters long')

        return value

    @field_validator('password')
    def password_min_lenght(cls, value):
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')

        return value


class UserPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    update_at: datetime


class UserListPublicSchema(BaseModel):
    users: List[UserPublicSchema]
    offset: int
    limit: int
