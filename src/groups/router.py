from fastapi import APIRouter, Path, Body, HTTPException, Depends
from typing import Annotated

from ..dependencies import SessionDep, authenticationDep
from ..exceptions import authentication_exception


from .schemas import GroupCreate, GroupResponse
from .services import create_group, delete_group, new_member

from ..config import settings

router = APIRouter(
    prefix="/group",
    tags=["Group"]
)


@router.post("/create", response_model=GroupResponse, status_code=201)
async def create(
    group_data: Annotated[GroupCreate, Body()],  
    session: SessionDep,
    access_token: Annotated[str, Body()],
    auth_service: authenticationDep
):
    
    user = await auth_service.api_auth(access_token, session) 

    if not user:
        raise authentication_exception


    group = await create_group(user.id, group_data, session)
    
    return group



@router.post("/delete/{group_id}", status_code=204)
async def delete(
    group_id: Annotated[int, Path()], 
    session: SessionDep,
    access_token: Annotated[str, Body()], 
    auth_service: authenticationDep
): 
    
    user = await auth_service.api_auth(access_token, session) 

    if not user:
        raise authentication_exception
     
    await delete_group(user.id, group_id, session)





@router.post("/add_member/{member_id}/group/{group_id}")
async def add_member(
    group_id: Annotated[int, Path()],
    member_id: Annotated[int, Path()],
    session: SessionDep,
    access_token: Annotated[str, Body()], 
    auth_service: authenticationDep
): 
    
    user = await auth_service.api_auth(access_token, session) 

    if not user:
        raise authentication_exception
    
    await new_member(member_id, group_id, session)



@router.post("/remove_member/{member_id}/group/{group_id}")
async def remove_member(
    group_id: Annotated[int, Path()], 
    member_id: Annotated[int, Path()], 
    session: SessionDep,
    access_token: Annotated[str, Body()], 
    auth_service: authenticationDep
): 
    
    user = await auth_service.api_auth(access_token, session) 

    if not user:
        raise authentication_exception