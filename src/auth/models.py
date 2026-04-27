from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from ..models import Base



class RefeshToken(Base):

    __tablename__   = "refresh_tokens"


    id:                 Mapped[int]         = mapped_column(primary_key=True)
    value:              Mapped[str]         = mapped_column(unique=True)
    user_id                                 = mapped_column(ForeignKey("users.id"))
    expire_date:        Mapped[datetime]
    blacked_listed:     Mapped[bool]        = mapped_column(default=False)
