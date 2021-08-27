from pydantic import BaseModel


class City(BaseModel):
    name: str

    class Config:
        orm_mode = True