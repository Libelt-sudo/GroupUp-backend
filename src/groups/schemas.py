from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True


class PollOptionCreate(BaseModel):
    text: str


class PollResponseCreate(BaseModel):
    option_id: int


class PollCreate(BaseModel):
    question: str
    options: list[PollOptionCreate]


class PollUpdate(BaseModel):
    question: str | None = None


class PollOptionResponse(BaseModel):
    id: int
    text: str
    poll_id: int

    class Config:
        from_attributes = True


class PollResponseOut(BaseModel):
    id: int
    poll_id: int
    option_id: int
    user_id: int

    class Config:
        from_attributes = True


class PollResponse(BaseModel):
    id: int
    question: str
    group_id: int
    created_by: int
    options: list[PollOptionResponse] = Field(default_factory=list)
    responses: list[PollResponseOut] = Field(default_factory=list)

    class Config:
        from_attributes = True
    