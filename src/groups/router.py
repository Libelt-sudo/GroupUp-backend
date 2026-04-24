from fastapi import APIRouter, Body, HTTPException, Depends
from typing import Annotated
from ..dependencies import SessionDep, authenticationDep
from ..exceptions import authentication_exception

from ..config import settings

router = APIRouter(
    prefix="/group",
    tags=["Group"]
)


@router.post("/create")
async def create_group(access_token: Annotated[str, Body()], session: SessionDep, auth_service: authenticationDep):
    print(access_token)
    user = await auth_service.api_auth(access_token, session)

    if not user:
        raise authentication_exception
    
    return {"message": "User is authenticated"}
    


@router.post("/delete")
async def delete_group(): 
    pass


@router.post("/add_member")
async def add_member(): 
    pass


@router.post("/remove_member")
async def remove_member(): 
    pass