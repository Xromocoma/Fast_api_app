from pydantic import BaseModel


class City(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CityInfo(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

