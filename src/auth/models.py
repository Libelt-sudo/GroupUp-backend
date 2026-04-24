from datetime import datetime

import typing
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from ..models import Base
from src.associations import group_members


if typing.TYPE_CHECKING:
    from ..groups.models import Group



class User(Base):
    
    __tablename__   = "users"


    id:                 Mapped[int]                 = mapped_column(primary_key=True, index=True)
    email:              Mapped[str]                 = mapped_column(unique=True)
    username:           Mapped[str]                 = mapped_column(String(30), unique=True)
    password_hash:      Mapped[str]

    groups_in:          Mapped[List["Group"]]       = relationship("Group", secondary=group_members, back_populates="members")


class RefeshToken(Base):

    __tablename__   = "refresh_tokens"


    id:                 Mapped[int]         = mapped_column(primary_key=True)
    value:              Mapped[str]         = mapped_column(unique=True)
    user_id                                 = mapped_column(ForeignKey("users.id"))
    expire_date:        Mapped[datetime]
    blacked_listed:     Mapped[bool]        = mapped_column(default=False)
