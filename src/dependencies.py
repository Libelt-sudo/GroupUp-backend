from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from .database import create_db_session

from .auth.services import AuthService

def get_auth_service():
    return AuthService()

SessionDep = Annotated[AsyncSession, Depends(create_db_session)]
authenticationDep = Annotated[AuthService, Depends(get_auth_service)]