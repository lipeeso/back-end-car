from typing import Optional, List
from pydantic import BaseModel, EmailStr

"""Para diferentes use cases podemos criar diferentes schemas, por exemplo, para criar um usuário, atualizar um usuário, etc."""


class UserSchema(BaseModel): 
    username: str
    email: EmailStr
    password: str


class UserPublicSchema(
    BaseModel
):  
    id: int
    username: str
    email: EmailStr


class UserUpdateSchema(
    BaseModel
): 
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserListPublicSchema(
    BaseModel
):  
    users: List[UserPublicSchema]
