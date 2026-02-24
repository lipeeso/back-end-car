from typing import Optional, List
from pydantic import BaseModel, EmailStr

"""Para diferentes use cases podemos criar diferentes schemas, por exemplo, para criar um usuário, atualizar um usuário, etc."""


class UserSchema(BaseModel):  # -> Representa a estrutura de dados para um usuário
    username: str
    email: EmailStr
    password: str


class UserPublicSchema(
    BaseModel
):  # -> Representa a estrutura de dados para um usuário público, ou seja, sem a senha
    id: int
    username: str
    email: EmailStr


class UserUpdateSchema(
    BaseModel
):  # -> Representa a estrutura de dados para atualizar um usuário, onde todos os campos são opcionais
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserListPublicSchema(
    BaseModel
):  # -> Representa a estrutura de dados para um usuário público, ou seja, vai retornar essa lista de usuário
    users: List[UserPublicSchema]
