from sqlalchemy import update, delete
from app.models import City
from app.core.database import db
from fastapi import status, HTTPException


def get_all_cities():
    session = db.session()
    cities = session.query(City).order_by(City.id)
    result = []
    for city in cities:
        result.append(city)
    return result


def get_city_by_name(city_name: str):
    session = db.session()
    return session.query(City).where(City.name == city_name).first()


def get_city_by_id(city_id: int):
    session = db.session()
    return session.query(City).where(City.id == city_id).first()


def city_add(city_name: str):
    if not city_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty city name')
    if get_city_by_name(city_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='this city name already exists')

    session = db.session()
    new_city = City(name=city_name)
    session.add(new_city)
    session.commit()
    return new_city


def city_update(city_id: int, city: dict):
    if not city['name']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='nothing to update, empty param')
    if not get_city_by_id(city_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='city with this Id not found')

    session = db.session()
    session.execute(update(City).where(City.id == city_id).values(name=city['name']))
    session.commit()
    return get_city_by_id(city_id)


def city_delete(city_id: int):
    if not get_city_by_id(city_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='city with this Id not found')

    session = db.session()
    session.execute(delete(City).where(City.id == city_id))
    session.commit()
    return True
