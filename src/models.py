from sqlalchemy import ForeignKey, Table, Column, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import typing
from typing import List

# from .associations import group_members



class Base(DeclarativeBase):
    pass




if typing.TYPE_CHECKING:
    from .groups.models import Group


group_members = Table(
    "group_members",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True)
)


class User(Base):
    
    __tablename__   = "users"


    id:                 Mapped[int]                 = mapped_column(primary_key=True, index=True)
    email:              Mapped[str]                 = mapped_column(unique=True)
    username:           Mapped[str]                 = mapped_column(String(30), unique=True)
    password_hash:      Mapped[str]

    groups_in:          Mapped[List["Group"]]       = relationship("Group", secondary=group_members, back_populates="members")


    def __repr__(self):
        return f"user_id:{self.id} -> {self.username}"