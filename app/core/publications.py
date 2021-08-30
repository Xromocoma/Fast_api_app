import sqlalchemy.exc
from sqlalchemy import update, or_, func

from app.core.authorization import auth
from app.core.user import get_user
from app.models import Publication
from app.core.database import db
from fastapi import status, HTTPException


def get_all_publications(sort: int = None, search_string: str = None, user: int = None, city: int = None):
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


def get_publication_by_name(publication_name: str):
    session = db.session()
    return session.query(Publication).where(Publication.name == publication_name, Publication.state == True).first()


def get_publication_by_id(publication_id: int):
    session = db.session()
    return session.query(Publication).where(Publication.id == publication_id, Publication.state == True).first()


def create_publication(publication: dict, token: str):
    print(111,token)
    user = auth.parse_jwt_token(token)
    if not get_user(user['id']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')

    session = db.session()
    new_publication = Publication(**publication, users=user['id'])
    session.add(new_publication)
    session.commit()
    return get_publication_by_id(new_publication.id)


def update_publication(publication_id: int, publication: dict, token: str):
    user = auth.parse_jwt_token(token)
    if not get_user(user['id']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    old_publication = get_publication_by_id(publication_id)
    if not old_publication:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='publication with this Id not found')
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig))


def delete_publication(publication_id: int, token: str):
    user = auth.parse_jwt_token(token)
    if not get_user(user['id']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    old_publication = get_publication_by_id(publication_id)
    if not old_publication:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='publication with this Id not found')
    if old_publication.users != user['id'] and user['is_admin'] == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Permission denied! not your publication')
    session = db.session()
    session.execute(update(Publication).where(Publication.id == publication_id).values(state=False))
    session.commit()
    return True
