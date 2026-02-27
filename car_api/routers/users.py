from fastapi import APIRouter, status

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
    response_model=UserPublicSchema
)
async def create_user(user: UserSchema):
    user_with_id = UserPublicSchema(**user.model_dump(), id=len(USERS) + 1) # -> Cria um novo usuário com um ID único, baseado no tamanho da lista de usuários
    USERS.append(user_with_id) # -> Adiciona o novo usuário à lista de usuários 
    return user_with_id # -> Retorna o usuário criado, sem a senha, pois estamos usando o UserPublicSchema como resposta 


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