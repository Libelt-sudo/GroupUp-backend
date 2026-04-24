from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from .models import User, RefeshToken
from .schemas import UserCreate, Token, TokenData
from ..config import settings

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")



def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


# Authenticates user login credentials 
async def authenticate(email: str, password: str, session) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        verify_password(password, DUMMY_HASH)
        return False
    
    if verify_password(password, user.password_hash):
        return user
    
    return False


# Creates refresh token to send to user and stores it in DB
# for future access token refresh
async def create_refresh_token(user_id, expires_delta: timedelta, session):

    if expires_delta:
        expire = datetime.now() + timedelta(days=expires_delta)
    else:
        expire = datetime.now() + timedelta(days=1)
    

    to_encode = {"user_id": user_id, "exp": expire}


    token_value = jwt.encode(payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    refresh_token = RefeshToken(
        value = token_value,
        expire_date = expire,
        user_id = user_id
    )

    session.add(refresh_token)

    await session.commit()
    await session.refresh(refresh_token)

    return Token(token_value=refresh_token.value, token_type="refresh_token")



def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now() + timedelta(minutes=10)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return Token(token_value=encoded_jwt, token_type="bearer")


# User registeration.
# Creates user model and saves it to DB 
async def create_user(user_data: UserCreate, session):

    user = User(
        email = user_data.email,
        username = user_data.username,
        password_hash = get_password_hash(user_data.password)
    )

    session.add(user)
    await session.commit()

    await session.refresh(user)
    return user


# Used in user registeration for checking if email is already taken / in use
async def email_exists(email: str ,session):
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none() is not None


# Used in user registeration for checking if username is already taken
async def username_exists(username: str, session):
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none() is not None


# Retireves User model via user_id
async def get_user(user_id: int, session):
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()



class AuthService:
    # api_auth is used for authenticating users before accessing an API
    async def api_auth(self, token, session):
        credentials_expection = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            user_id = payload.get("user_id")
            if user_id is None:
                print("user_id is none")
                return False
            token_data = TokenData(user_id=user_id)
        except InvalidTokenError:
            print("This key is invalid")
            return False

        user = await get_user(token_data.user_id, session)

        if user is None:
            print("user is none")
            return False
        
        return user