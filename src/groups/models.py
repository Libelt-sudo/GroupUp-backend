from datetime import datetime

import typing
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from ..models import Base, group_members
# from src.associations import group_members


if typing.TYPE_CHECKING:
    from ..models import User



class Group(Base):

    __tablename__ = "groups"


    id:             Mapped[int]                 = mapped_column(primary_key=True)
    name:           Mapped[str]                 = mapped_column(String(30))
    owner_id                                    = mapped_column(ForeignKey("users.id"))
    
    members:        Mapped[List["User"]]        = relationship("User", secondary=group_members, back_populates="groups_in")

