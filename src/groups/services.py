from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from ..config import settings 

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Group
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


async def delete_group(user_id: int, group_id: int, session: AsyncSession):

    group_result   =   await session.execute(select(Group).where(Group.id == group_id))
    group          =   group_result.scalar_one_or_none()

    if not group:
        # raise an exception that group does not exist (404)
        pass

    if user_id == group_id:
        session.delete(group)
        session.commit()
    


async def new_member(member_id: int, group_id: int, session: AsyncSession):

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
    print(f"\n\n\n{group.members}\n\n\n")


    