from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from car_api.core.database import get_session
from car_api.core.security import get_current_user, get_password_hash
from car_api.models.users import User
from car_api.schemas.users import (
    UserListPublicSchema,
    UserPublicSchema,
    UserSchema,
    UserUpdateSchema,
)

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicSchema,
    summary='Create a new user',
)
async def create_user(
    user: UserSchema, db: AsyncSession = Depends(get_session)
):
    user_exists = await db.scalar(
        select(exists().where(User.username == user.username))
    )

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already exists',
        )

    email_exists = await db.scalar(
        select(exists().where(User.email == user.email))
    )

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already exists',
        )

    new_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=UserListPublicSchema,
    summary='List all users',
)
async def list_users(
    offset: int = Query(0, ge=0, description='Number of items to skip'),
    limit: int = Query(
        100, ge=1, le=100, description='Maximum number of items to return'
    ),
    search: Optional[str] = Query(
        None, description='Search term for username or email'
    ),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):

    query = select(User)

    if search:
        search_filter = f'%{search}%'
        query = query.where(
            User.username.ilike(search_filter)
            | User.email.ilike(search_filter)
        )

    query = query.offset(offset).limit(
        limit
    )  # -> Aplica o deslocamento e o limite à consulta SQLAlchemy.
    result = await db.execute(query)
    users = result.scalars().all()
    return {
        'users': users,
        'offset': offset,
        'limit': limit,
    }


@router.get(
    path='/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    summary='Get a user by ID',
)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    return user


@router.put(
    path='/{user_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicSchema,
    summary='Update a user by ID',
)
async def update_user(
    user_id: int,
    user_update: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):

    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    update_data = user_update.model_dump(exclude_unset=True)

    if 'username' in update_data and update_data['username'] != user.username:
        user_exists = await db.scalar(
            select(
                exists().where(
                    (User.username == update_data['username'])
                    & (User.id != user_id)
                )
            )
        )
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists',
            )

    if 'email' in update_data and update_data['email'] != user.email:
        email_exists = await db.scalar(
            select(
                exists().where(
                    (User.email == update_data['email']) & (User.id != user_id)
                )
            )
        )
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already exists',
            )

    if 'password' in update_data:
        update_data['password'] = get_password_hash(update_data['password'])

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


@router.delete(
    path='/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a user by ID',
)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    user = await db.get(
        User, user_id
    )  # -> Obtem o objeto do usuário com o ID fornecido

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    await db.delete(user)
    await db.commit()
