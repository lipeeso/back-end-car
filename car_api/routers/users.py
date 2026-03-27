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
        select(exists().where(User.username == user.username))
    )

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username or email already exists'
        )
    
    email_exists = await db.scalar(select(exists().where(User.email == user.email)))

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='email already exists'
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
    response_model=UserListPublicSchema,
    summary='List all users'
)
async def list_users(
    db: AsyncSession = Depends(get_session)
):  
    
    users = await db.execute(select(User))
    users_list = users.scalars().all()

    if not users_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No users found'
        )
    
    return {"users": users_list} 

@router.put(
    path='/{user_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicSchema,
)
async def update_user(user_id: int, user: UserSchema):
    pass
    

@router.delete(
    path='/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT  
)
async def delete_user(user_id: int):
    del USERS[user_id - 1]
    return None # -> Retorna None, pois o status code 204 indica que a operação foi bem-sucedida, mas não há conteúdo para retornar