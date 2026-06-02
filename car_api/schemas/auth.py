from pydantic import BaseModel, EmailStr, field_validator


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    def password_min_lenght(cls, value):
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')

        return value
