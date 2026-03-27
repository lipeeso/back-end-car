from fastapi import APIRouter, status, HTTPException, Depends
from car_api.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from car_api.models.users import User
from car_api.schemas.users import (
    UserListPublicSchema, 
    UserSchema,
    UserPublicSchema,
)

from car_api.db import USERS

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicSchema,
    summary='Create a new user'
)
async def create_user(
    user: UserSchema,
    db: AsyncSession = Depends(get_session)
):
    user_exists = await db.scalar(
        select(exists().where(User.username == user.username or User.email == user.email))
    )

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username or email already exists'
        )
    
    new_user = User(
        username = user.username,
        password = user.password,
        email = user.email
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get(
    path='/',
    status_code=status.HTTP_200_OK, 
    response_model=UserListPublicSchema
)
async def list_users():
     return {"users": USERS} # -> Retorna a lista de usuários, sem as senhas, pois estamos usando o UserListPublicSchema como resposta

'''Sempre ou ter que sobrescrever o usuário inteiro, ou seja, enviar todos os campos, mesmo os que não foram alterados, ou podemos criar um endpoint para atualizar apenas um campo específico, por exemplo, apenas o email.'''
@router.put(
    path='/{user_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicSchema
)
async def update_user(user_id: int, user: UserSchema):
    user_with_id = UserPublicSchema(**user.model_dump(), id=user_id) # -> Cria um novo usuário com o ID fornecido e os dados do usuário atualizado
    USERS[user_id - 1] = user_with_id
    return user_with_id # -> Retorna o usuário atualizado, sem a senha, pois estamos usando o UserPublicSchema como resposta

@router.delete(
    path='/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT  
)
async def delete_user(user_id: int):
    del USERS[user_id - 1]
    return None # -> Retorna None, pois o status code 204 indica que a operação foi bem-sucedida, mas não há conteúdo para retornar