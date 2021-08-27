from pydantic import BaseModel
from typing import Union


class PublicationDelete(BaseModel):
    id: int

    class Config:
        orm_mode = True


class PublicationCreate(BaseModel):
    name: str
    users: int
    city: int
    body: str
    price: float

    class Config:
        orm_mode = True


class Publication(PublicationCreate):
    state: bool


class PublicationUpdate(BaseModel):
    name: Union[str, None]
    users: Union[int, None]
    city: Union[int, None]
    body: Union[str, None]
    price: Union[float, None]
    state: Union[bool, None]

    class Config:
        orm_mode = True

