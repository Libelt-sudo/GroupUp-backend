from fastapi import APIRouter, Body, HTTPException
from typing import Annotated
from ..dependencies import SessionDep

from pydantic import EmailStr

from ..config import settings
from .models import RefeshToken
from .schemas import UserCreate, UserResponse
from .exceptions import EmailExistsException, UsernameExistsException
from .services import (
    create_user, 
    authenticate, 
    create_access_token, 
    create_refresh_token,
    email_exists,
    username_exists
)



router = APIRouter(
    prefix="/auth",
    tags=["User Authentication"]
)



@router.post("/login", status_code=200)
async def login(email: EmailStr, password: str, session: SessionDep):
    user = await authenticate(email, password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token({"user_id": user.id}, settings.ACCESS_TOKEN_EXPIRE_M)
    refresh_token = await create_refresh_token(user.id, settings.REFRESH_TOKEN_EXPIRE_D, session)

    return {"access": access_token, "refresh": refresh_token}
    


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: Annotated[UserCreate, Body()], session: SessionDep):

    if await username_exists(user.username, session):
        raise UsernameExistsException

    if await email_exists(user.email, session):
        raise EmailExistsException

    return await create_user(user, session)



@router.post("/logout", status_code=200)
async def logout():
    pass