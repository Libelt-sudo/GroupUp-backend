from pydantic import BaseModel, EmailStr, Field



class UserBase(BaseModel):
    email:          EmailStr
    username:       str


class UserCreate(UserBase):
    password:       str


class UserResponse(UserBase):
    id:             int


class UserDB(UserBase):
    password_hash:  str


class Token(BaseModel):
    token_value:    str
    token_type:     str


class TokenData(BaseModel):
    user_id:        int | None = None
