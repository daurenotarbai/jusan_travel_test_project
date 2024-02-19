import uuid

from pydantic.networks import EmailStr

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
