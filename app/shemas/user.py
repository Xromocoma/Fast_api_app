from pydantic import BaseModel
from typing import Union


class UserLogin(BaseModel):
    login: str
    passwd: str


class UserData(BaseModel):
    login: str
    name: str
    city: int
    state: bool = True
    is_admin: bool = False

    class Config:
        orm_mode = True


class UserCreate(UserData):
    passwd: str


class UserInfo(UserData):
    id: int


class UserFullData(UserInfo):
    passwd: str


class UserUpdate(BaseModel):
    login: Union[str, None]
    passwd: Union[str, None]
    name: Union[str, None]
    city: Union[int, None]
    state: Union[bool, None]
    is_admin: Union[bool, None]

    class Config:
        orm_mode = True



