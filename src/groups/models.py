from datetime import datetime

import typing
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from ..models import Base


if typing.TYPE_CHECKING:
    from ..auth.models import User



class Group(Base):

    __tablename__ = "groups"


    id:             Mapped[int]                 = mapped_column(primary_key=True)
    name:           Mapped[str]                 = mapped_column(String(30))
    owner_id                                    = mapped_column(ForeignKey("memberships.id"))

    members:        Mapped[List["Membership"]]  = relationship("Membership", foreign_keys="[Membership.group_id]", back_populates="group")
    

class Membership(Base):

    __tablename__ = "memberships"
    

    id:             Mapped[int]         = mapped_column(primary_key=True)
    is_admin:       Mapped[bool]            

    user_id                             = mapped_column(ForeignKey("users.id"))
    user:           Mapped["User"]      = relationship("User", back_populates="group_memberships")

    group_id                            = mapped_column(ForeignKey("groups.id"))
    group :         Mapped["Group"]     = relationship("Group", foreign_keys=[group_id], back_populates="members")

    
