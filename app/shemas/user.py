from pydantic import BaseModel
from typing import Union


class UserLogin(BaseModel):
    login: str
    passwd: str

    class Config:
        orm_mode = True


class UserData(BaseModel):
    name: str
    city: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    login: str
    name: str
    city: int
    passwd: str

    class Config:
        orm_mode = True


class UserInfo(BaseModel):
    id: int
    name: str
    city: int

    class Config:
        orm_mode = True


class UserFullData(BaseModel):
    id: int
    login: str
    passwd: str
    name: str
    city: int
    is_admin: bool
    state: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    login: Union[str, None]
    passwd: Union[str, None]
    name: Union[str, None]
    city: Union[int, None]

    class Config:
        orm_mode = True


class UserSetAdmin(BaseModel):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True
