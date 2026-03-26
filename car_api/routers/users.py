from fastapi import APIRouter, status, Depends
from car_api.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
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
    db_user = User(
        username=user.username,
        password=user.password,
        email=user.email
    )
    
    db.add(db_user) # -> Adiciona o novo usuário à sessão do banco de dados apenas na memória, ainda não foi salvo no banco de dados
    await db.commit() # -> Salva as alterações no banco de dados, ou seja,
    await db.refresh(db_user) # -> Atualiza o objeto do usuário com os dados do banco de dados, incluindo o ID gerado automaticamente
    return db_user # -> Retorna o usuário criado, sem a senha, pois estamos usando

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