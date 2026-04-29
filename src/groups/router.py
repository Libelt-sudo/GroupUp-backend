from fastapi import APIRouter, Path, Body, HTTPException, Depends, Header
from typing import Annotated

from ..dependencies import SessionDep, authenticationDep
from ..exceptions import authentication_exception


from .schemas import (
    GroupCreate,
    GroupResponse,
    PollCreate,
    PollUpdate,
    PollResponse,
    PollResponseCreate,
    PollResponseOut,
)
from .services import (
    create_group as create_group_service,
    delete_group as delete_group_service,
    add_member as add_member_service,
    remove_member as remove_member_service,
    create_poll as create_poll_service,
    get_poll as get_poll_service,
    update_poll as update_poll_service,
    delete_poll as delete_poll_service,
    add_poll_response as add_poll_response_service,
    get_poll_responses as get_poll_responses_service,
    delete_poll_response as delete_poll_response_service,
)

from ..config import settings

router = APIRouter(
    prefix="/group",
    tags=["Group"]
)


@router.post("/create", response_model=GroupResponse, status_code=201)
async def create(
    group_data: Annotated[GroupCreate, Body()],  
    session: SessionDep,
    access_token: Annotated[str, Header()],
    auth_service: authenticationDep
):
    
    user = await auth_service.api_auth(access_token, session) 

    if not user:
        raise authentication_exception


    group = await create_group_service(user.id, group_data, session)
    
    return group



@router.delete("/delete/{group_id}", status_code=204)
async def delete(
    group_id: Annotated[int, Path()], 
    session: SessionDep,
    access_token: Annotated[str, Header()], 
    auth_service: authenticationDep
): 
    
    user = await auth_service.api_auth(access_token, session) 

    if not user:
        raise authentication_exception
     
    await delete_group_service(user.id, group_id, session)



@router.post("/add_member/{member_id}/group/{group_id}", status_code=200)
async def add_member(
    group_id: Annotated[int, Path()],
    member_id: Annotated[int, Path()],
    session: SessionDep,
    access_token: Annotated[str, Header()], 
    auth_service: authenticationDep
): 
    
    user = await auth_service.api_auth(access_token, session) 

    if not user:
        raise authentication_exception
    
    await add_member_service(member_id, group_id, session)



@router.post("/remove_member/{member_id}/group/{group_id}", status_code=204)
async def remove_member(
    group_id: Annotated[int, Path()], 
    member_id: Annotated[int, Path()], 
    session: SessionDep,
    access_token: Annotated[str, Header()], 
    auth_service: authenticationDep
): 

    user = await auth_service.api_auth(access_token, session) 

    if not user:
        raise authentication_exception
    
    await remove_member_service(member_id, group_id, session)


@router.post("/{group_id}/poll", response_model=PollResponse, status_code=201)
async def create_poll(
    group_id: Annotated[int, Path()],
    poll_data: Annotated[PollCreate, Body()],
    session: SessionDep,
    access_token: Annotated[str, Header()],
    auth_service: authenticationDep
):
    user = await auth_service.api_auth(access_token, session)

    if not user:
        raise authentication_exception

    poll = await create_poll_service(group_id, user.id, poll_data, session)
    return poll


@router.get("/poll/{poll_id}", response_model=PollResponse)
async def get_poll(
    poll_id: Annotated[int, Path()],
    session: SessionDep,
    access_token: Annotated[str, Header()],
    auth_service: authenticationDep
):
    user = await auth_service.api_auth(access_token, session)

    if not user:
        raise authentication_exception

    return await get_poll_service(poll_id, session)


@router.patch("/poll/{poll_id}", response_model=PollResponse)
async def update_poll(
    poll_id: Annotated[int, Path()],
    poll_update: Annotated[PollUpdate, Body()],
    session: SessionDep,
    access_token: Annotated[str, Header()],
    auth_service: authenticationDep
):
    user = await auth_service.api_auth(access_token, session)

    if not user:
        raise authentication_exception

    return await update_poll_service(poll_id, user.id, poll_update, session)


@router.delete("/poll/{poll_id}", status_code=204)
async def delete_poll(
    poll_id: Annotated[int, Path()],
    session: SessionDep,
    access_token: Annotated[str, Header()],
    auth_service: authenticationDep
):
    user = await auth_service.api_auth(access_token, session)

    if not user:
        raise authentication_exception

    await delete_poll_service(poll_id, user.id, session)


@router.post("/poll/{poll_id}/response", response_model=PollResponseOut, status_code=201)
async def add_poll_response(
    poll_id: Annotated[int, Path()],
    response_data: Annotated[PollResponseCreate, Body()],
    session: SessionDep,
    access_token: Annotated[str, Header()],
    auth_service: authenticationDep
):
    user = await auth_service.api_auth(access_token, session)

    if not user:
        raise authentication_exception

    return await add_poll_response_service(poll_id, user.id, response_data, session)


@router.get("/poll/{poll_id}/responses", response_model=list[PollResponseOut])
async def get_poll_responses(
    poll_id: Annotated[int, Path()],
    session: SessionDep,
    access_token: Annotated[str, Header()],
    auth_service: authenticationDep
):
    user = await auth_service.api_auth(access_token, session)

    if not user:
        raise authentication_exception

    return await get_poll_responses_service(poll_id, session)


@router.delete("/poll/{poll_id}/response", status_code=204)
async def delete_poll_response(
    poll_id: Annotated[int, Path()],
    session: SessionDep,
    access_token: Annotated[str, Header()],
    auth_service: authenticationDep
):
    user = await auth_service.api_auth(access_token, session)

    if not user:
        raise authentication_exception

    await delete_poll_response_service(poll_id, user.id, session)
