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
     return {
        'users': [
            {
                'id': 1,
                'username': 'pycodebr',
                'email': 'pycodebr@gmail.com',
            },
            {
                'id': 2,
                'username': 'joao',
                'email': 'joao@gmail.com',
            },
            {
                'id': 3,
                'username': 'mario',
                'email': 'mario@gmail.com',
            },
        ]
    }
