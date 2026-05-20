from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from typing import Dict, Optional

from pwdlib import PasswordHash
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from car_api.models.users import User   
from car_api.core.settings import Settings
from car_api.core.database import get_session

security = HTTPBearer()
settings = Settings()

pwd_context = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


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

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_session)
)-> User:
    
    payload = verify_token(credentials.credentials)

    user_id_str = payload.get('sub')

    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token: missing user ID',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    try:

        user_id = int(user_id_str)
    
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token: user ID must be an integer',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
        
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user