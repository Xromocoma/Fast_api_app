from typing import List
import sqlalchemy.exc
from sqlalchemy import update, delete
from fastapi import status, HTTPException
from app.models import City
from app.core.database import db


def get_all_cities() -> List[City]:
    """
    Получение списка всех городов
    :return: List[City]
    """
    session = db.session()
    cities = session.query(City).order_by(City.id)
    result = []
    for city in cities:
        result.append(city)
    return result


def get_city_by_name(city_name: str) -> City:
    """
    Получение города по ID
    :param city_name:
    :return: City
    """
    session = db.session()
    return session.query(City).where(City.name == city_name).first()


def get_city_by_id(city_id: int) -> City:
    """
    Проверка и получение города по ID
    :param city_id:
    :return: City
    """
    session = db.session()
    res = session.query(City).where(City.id == city_id).first()
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='city with this Id not found')
    return res


def city_add(city_name: str) -> City:
    """
    Добавление города
    :param city_name:
    :return: City
    """
    if not city_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='empty city name')
    if get_city_by_name(city_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='this city name already exists')

    session = db.session()
    new_city = City(name=city_name)
    session.add(new_city)
    session.commit()
    return new_city


def city_update(city_id: int, city: dict) -> City:
    """
    Обновление имени города
    :param city_id:
    :param city:
    :return: City
    """
    if city_id == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='can`t update default city')
    if not city['name']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='nothing to update, empty param')
    get_city_by_id(city_id)

    session = db.session()
    session.execute(update(City).where(City.id == city_id).values(name=city['name']))
    session.commit()
    return get_city_by_id(city_id)


def city_delete(city_id: int) -> bool:
    """
    Удаление города
    :param city_id:
    :return: bool
    """
    if city_id == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='can`t delete default city')

    get_city_by_id(city_id)
    session = db.session()
    try:
        session.execute(delete(City).where(City.id == city_id))
        session.commit()
        return True
    except sqlalchemy.exc.IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig)) from e
