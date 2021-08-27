from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey

from app.core.database import db


class City(db.base):
    __tablename__ = 'City'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class User(db.base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    passwd = Column(String)
    name = Column(String)
    city = Column(Integer, ForeignKey(City.id))
    state = Column(Boolean, default=1)
    is_admin = Column(Boolean, default=0),


class Publication(db.base):
    __tablename__ = 'Publication'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = Column(Integer, ForeignKey(User.id))
    city = Column(Integer, ForeignKey(City.id))
    body = Column(String)
    price = Column(Float)
    state = Column(Boolean, default=1)
