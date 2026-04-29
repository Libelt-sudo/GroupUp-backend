from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from ..config import settings 

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Group, Poll, PollOption, PollResponse as PollResponseModel
from ..models import User


async def create_group(user_id, data, session: AsyncSession):
    
    group = Group(
        name = data.name,
        owner_id = user_id
    )

    owner_result    = await session.execute(select(User).where(User.id == user_id))
    owner           = owner_result.scalar_one_or_none()

    group.members.append(owner)

    session.add(group)
    await session.commit()

    await session.refresh(group)
    return group


async def create_poll(group_id: int, user_id: int, data, session: AsyncSession):
    group_result = await session.execute(
        select(Group)
        .where(Group.id == group_id)
        .options(selectinload(Group.members))
    )
    group = group_result.scalar_one_or_none()

    if not group:
        raise HTTPException(status_code=404, detail="Group does not exist")

    if all(member.id != user_id for member in group.members):
        raise HTTPException(status_code=403, detail="User is not a member of this group")

    poll = Poll(question=data.question, group_id=group_id, created_by=user_id)
    poll.options = [PollOption(text=option.text) for option in data.options]

    session.add(poll)
    await session.commit()
    await session.refresh(poll)

    # Reload with relationships
    poll_result = await session.execute(
        select(Poll)
        .where(Poll.id == poll.id)
        .options(selectinload(Poll.options), selectinload(Poll.responses))
    )
    poll = poll_result.scalar_one()
    return poll


async def get_poll(poll_id: int, session: AsyncSession):
    poll_result = await session.execute(
        select(Poll)
        .where(Poll.id == poll_id)
        .options(selectinload(Poll.options), selectinload(Poll.responses))
    )
    poll = poll_result.scalar_one_or_none()

    if not poll:
        raise HTTPException(status_code=404, detail="Poll does not exist")

    return poll


async def update_poll(poll_id: int, user_id: int, data, session: AsyncSession):
    poll = await get_poll(poll_id, session)

    if poll.created_by != user_id:
        raise HTTPException(status_code=403, detail="Only the poll creator can update this poll")

    if data.question is not None:
        poll.question = data.question

    await session.commit()
    await session.refresh(poll)
    return poll


async def delete_poll(poll_id: int, user_id: int, session: AsyncSession):
    poll_result = await session.execute(select(Poll).where(Poll.id == poll_id))
    poll = poll_result.scalar_one_or_none()

    if not poll:
        raise HTTPException(status_code=404, detail="Poll does not exist")

    if poll.created_by != user_id:
        raise HTTPException(status_code=403, detail="Only the poll creator can delete this poll")

    await session.delete(poll)
    await session.commit()


async def add_poll_response(poll_id: int, user_id: int, data, session: AsyncSession):
    poll_result = await session.execute(select(Poll).where(Poll.id == poll_id))
    poll = poll_result.scalar_one_or_none()

    if not poll:
        raise HTTPException(status_code=404, detail="Poll does not exist")

    existing_response_result = await session.execute(
        select(PollResponseModel)
        .where(PollResponseModel.poll_id == poll_id, PollResponseModel.user_id == user_id)
    )
    if existing_response_result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="User has already responded to this poll")

    option_result = await session.execute(
        select(PollOption)
        .where(PollOption.id == data.option_id, PollOption.poll_id == poll_id)
    )
    option = option_result.scalar_one_or_none()

    if not option:
        raise HTTPException(status_code=404, detail="Option does not exist for this poll")

    response = PollResponseModel(poll_id=poll_id, option_id=data.option_id, user_id=user_id)
    session.add(response)
    await session.commit()
    await session.refresh(response)
    return response


async def get_poll_responses(poll_id: int, session: AsyncSession):
    poll_exists = await session.execute(select(Poll).where(Poll.id == poll_id))
    if poll_exists.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Poll does not exist")

    responses_result = await session.execute(
        select(PollResponseModel).where(PollResponseModel.poll_id == poll_id)
    )
    return responses_result.scalars().all()


async def delete_poll_response(poll_id: int, user_id: int, session: AsyncSession):
    response_result = await session.execute(
        select(PollResponseModel)
        .where(PollResponseModel.poll_id == poll_id, PollResponseModel.user_id == user_id)
    )
    response = response_result.scalar_one_or_none()

    if not response:
        raise HTTPException(status_code=404, detail="Vote not found")

    await session.delete(response)
    await session.commit()


async def delete_group(user_id: int, group_id: int, session: AsyncSession):

    group_result   =   await session.execute(select(Group).where(Group.id == group_id))
    group          =   group_result.scalar_one_or_none()

    if not group:
        # raise an exception that group does not exist (404)
        pass

    if user_id == group_id:
        session.delete(group)
        session.commit()
    


async def add_member(member_id: int, group_id: int, session: AsyncSession):

    member_result  =   await session.execute(select(User).where(User.id == member_id))
    member         =   member_result.scalar_one_or_none()

    group_result   =   await session.execute(select(Group).where(Group.id == group_id).options(selectinload(Group.members)))
    group          =   group_result.scalar_one_or_none()


    if not member:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not group:
        raise HTTPException(status_code=404, detail="Group does not exist")

    if member in group.members:
        raise HTTPException(status_code=409, detail="User is already a member of this group")

    group.members.append(member)
    await session.commit()



async def remove_member(member_id: int, group_id: int, session: AsyncSession):

    member_result  =   await session.execute(select(User).where(User.id == member_id))
    member         =   member_result.scalar_one_or_none()

    group_result   =   await session.execute(select(Group).where(Group.id == group_id).options(selectinload(Group.members)))
    group          =   group_result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not group:
        raise HTTPException(status_code=404, detail="Group does not exist")

    if member not in group.members:
        raise HTTPException(status_code=409, detail="User is not a member of this group")


    group.members.remove(member)

    await session.commit()


