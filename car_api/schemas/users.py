from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from datetime import datetime
"""Para diferentes use cases podemos criar diferentes schemas, por exemplo, para criar um usuário, atualizar um usuário, etc."""


class UserSchema(BaseModel): 
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    def username_min_lenght(cls, value):
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        return value

    @field_validator("password")
    def password_min_lenght(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        return value
    
class UserUpdateSchema(
    BaseModel
): 
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator("username")
    def username_min_lenght(cls, value):
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        return value

    @field_validator("password")
    def password_min_lenght(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        return value


class UserPublicSchema(
    BaseModel
):
    model_config = ConfigDict(from_attributes=True)  #esse schema pode ser criado lendo atributos de um objeto, não só chaves de um dicionário. permite converter objetos ORM/classes em schema de resposta.
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    update_at: datetime


class UserListPublicSchema(
    BaseModel
):  
    users: List[UserPublicSchema]
    offset: int
    limit: int
