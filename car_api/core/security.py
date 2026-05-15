from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from pwdlib import PasswordHash
import jwt

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

