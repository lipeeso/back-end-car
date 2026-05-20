from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from typing import Dict, Optional

from pwdlib import PasswordHash
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from car_api.models.users import User   
from car_api.core.settings import Settings

settings = Settings()

pwd_context = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

'''Authentication for users'''
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data:Dict)-> str:

    to_encode =  data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        payload=to_encode, 
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt

def verify_token(token:str)-> Dict:
    try:

        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token has expired',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
async def authenticate_user(
    email: str, password: str, db: AsyncSession
    ) -> Optional[User]:

    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None 
    
    return user