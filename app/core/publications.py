from sqlalchemy import update, delete
from app.models import Publication
from app.core.database import db
from fastapi import status, HTTPException


def get_all_publications():
    session = db.session()
    publications = session.query(Publication).where(Publication.state == True).order_by(Publication.id)
    result = []
    for publication in publications:
        result.append(publication)
    return result


def get_publication_by_name(publication_name: str):
    session = db.session()
    return session.query(Publication).where(Publication.name == publication_name).first()


def get_publication_by_id(publication_id: int):
    session = db.session()
    return session.query(Publication).where(Publication.id == publication_id).first()


def create_publication(publication: dict):
    session = db.session()
    new_publication = Publication(**publication)
    session.add(new_publication)
    session.commit()
    return get_publication_by_id(new_publication.id)


def update_publication(publication_id: int, publication: dict):
    if not get_publication_by_id(publication_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='publication with this Id not found')
    update_values = {}
    for item in publication:
        if publication[item] is not None and publication[item] != '':
            update_values.update({item: publication[item]})
    session = db.session()
    session.execute(update(Publication).where(Publication.id == publication_id).values(**update_values))
    session.commit()
    return get_publication_by_id(publication_id)


def delete_publication(publication_id: int):
    if not get_publication_by_id(publication_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='publication with this Id not found')

    session = db.session()
    session.execute(delete(Publication).where(Publication.id == publication_id))
    session.commit()
    return True
