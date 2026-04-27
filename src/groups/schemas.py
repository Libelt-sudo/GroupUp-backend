from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    