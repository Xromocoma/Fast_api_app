from typing import List
import sqlalchemy.exc
from sqlalchemy import update, or_, func
from fastapi import status, HTTPException
from app.core.authorization import auth
from app.core.user import get_user
from app.models import Publication
from app.core.database import db


def get_all_publications(sort: int = None,
                         search_string: str = None,
                         user: int = None,
                         city: int = None) -> List[Publication]:
    """
    Получение списка всех публикаций, предусмотрена возможность использования фильтров.
    :param sort: Optional
    :param search_string: Optional
    :param user: Optional
    :param city: Optional
    :return: List[Publication]
    """
    session = db.session()
    query = session.query(Publication).where(Publication.state == True)

    if search_string:
        query = query.filter(or_(
            func.similarity(Publication.name, search_string) > 0.3,
            func.similarity(Publication.body, search_string) > 0.2,
        ), )
    if city:
        query = query.filter(Publication.city == city)
    if user:
        query = query.filter(Publication.users == user)

    if sort:
        if sort == 1:
            query = query.order_by(Publication.id.asc())
        elif sort == -1:
            query = query.order_by(Publication.id.desc())

    query = query.all()
    return query


def get_publication_by_id(publication_id: int) -> Publication:
    """
    Получение публикации по ID
    :param publication_id:
    :return: Publication:
    """
    session = db.session()
    res =  session.query(Publication).where(Publication.id == publication_id, Publication.state == True).first()
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='publication with this Id not found')
    return res


def create_publication(publication: dict, token: str) -> Publication:
    """
    Создание объявления
    :param publication:
    :param token:
    :return: Publication:
    """
    user = auth.parse_jwt_token(token)
    get_user(user['id'])  # Проверка на наличие юзера указанного в токене

    session = db.session()
    try:
        new_publication = Publication(**publication, users=user['id'])
        session.add(new_publication)
        session.commit()
        return get_publication_by_id(new_publication.id)
    except sqlalchemy.exc.IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig)) from e


def update_publication(publication_id: int, publication: dict, token: str) -> Publication:
    """
    Обновление публикации
    :param publication_id:
    :param publication:
    :param token:
    :return: Publication
    """

    user = auth.parse_jwt_token(token)
    get_user(user['id'])  # Проверка на наличие юзера указанного в токене

    old_publication = get_publication_by_id(publication_id)  # Проверка и получение объявления

    # Проверка на создателя события, если событие не твое и ты не админ, ты не можешь его редактировать
    if user['is_admin'] == False and old_publication.users != user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied! not your publication')
    update_values = {}
    for item in publication:
        if publication[item] is not None and publication[item] != '':
            update_values.update({item: publication[item]})

    if not update_values:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='nothing to update, body empty.')
    session = db.session()
    try:
        session.execute(update(Publication).where(Publication.id == publication_id).values(**update_values))
        session.commit()
        return get_publication_by_id(publication_id)
    except sqlalchemy.exc.IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig)) from e


def delete_publication(publication_id: int, token: str) -> bool:
    """
    Удаление объявления
    :param publication_id:
    :param token:
    :return: bool
    """
    user = auth.parse_jwt_token(token)
    get_user(user['id'])  # Проверка наличия пользователя

    old_publication = get_publication_by_id(publication_id)  # Проверка и получение объявления

    if old_publication.users != user['id'] and user['is_admin'] == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied! not your publication')
    session = db.session()
    session.execute(update(Publication).where(Publication.id == publication_id).values(state=False))
    session.commit()
    return True
