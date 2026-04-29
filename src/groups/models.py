from datetime import datetime

import typing
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, UniqueConstraint

from ..models import Base, group_members


if typing.TYPE_CHECKING:
    from ..models import User



class Group(Base):

    __tablename__ = "groups"


    id:             Mapped[int]             = mapped_column(primary_key=True)
    name:           Mapped[str]             = mapped_column(String(30))
    owner_id                                = mapped_column(ForeignKey("users.id"))
    
    members:        Mapped[List["User"]]    = relationship("User", secondary=group_members, back_populates="groups_in")

    def __repr__(self):
        return f"group_id: {self.id} -> {self.name}"
    


class Poll(Base):

    __tablename__ = "polls"

    id:             Mapped[int]                     = mapped_column(primary_key=True)
    question:       Mapped[str]                     = mapped_column(String(150))
    group_id                                        = mapped_column(ForeignKey("groups.id"))
    created_by                                      = mapped_column(ForeignKey("users.id"))


    options:        Mapped[List["PollOption"]]      = relationship(back_populates="poll", cascade="all, delete-orphan")
    responses:      Mapped[List["PollResponse"]]    = relationship(back_populates="poll", cascade="all, delete-orphan")



class PollOption(Base):

    __tablename__ = "poll_options"

    id:         Mapped[int]     = mapped_column(primary_key=True)
    text:       Mapped[str]     = mapped_column(String(30))
    poll_id                     = mapped_column(ForeignKey("polls.id", ondelete="CASCADE"))

    poll:   Mapped[Poll]    = relationship(back_populates="options") 



class PollResponse(Base):
    __tablename__ = "poll_responses"

    id:         Mapped[int]     = mapped_column(primary_key=True)
    poll_id                     = mapped_column(ForeignKey("polls.id", ondelete="CASCADE"))
    option_id                   = mapped_column(ForeignKey("poll_options.id", ondelete="CASCADE"))
    user_id                     = mapped_column(ForeignKey("users.id"))

    poll:       Mapped[Poll]    = relationship(back_populates="responses")

    __table_args__ = (UniqueConstraint("poll_id", "user_id"),)
    
