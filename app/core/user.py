import hashlib
import json
from typing import List

import sqlalchemy.exc
from fastapi import HTTPException, status
from sqlalchemy import update

from app.shemas.user import UserCreate, UserLogin, UserInfo
from app.models import User
from app.core.database import db
from app.core.authorization import auth


def get_all_users() -> List[UserInfo]:
    """
    Получение списка всех юзеров
    :return: List[User]
    """
    session = db.session()
    users = session.query(User).where(User.state == True)
    result = []
    for user in users:
        result.append(UserInfo.from_orm(user))
    return result


def get_user(user_id: int) -> User:
    """
    Получить юзера по ID
    :param user_id:
    :return: User
    """
    session = db.session()
    user = session.query(User).where(User.id == user_id, User.state == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    return user


def update_user(user_id: int, update_params: dict, token: str) -> User:
    """
    Обновить юзера по ID, обновляемые поля динамические.
    :param user_id:
    :param update_params:
    :param token:
    :return: bool
    """
    user = auth.parse_jwt_token(token)
    if user['id'] == user_id:
        if not get_user(user['id']):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    else:
        if not get_user(user['id']):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
        if not get_user(user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')

    if user['id'] != user_id and user['is_admin'] == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
    # создаем новый dict с НЕ пустыми значениями для апдейта
    update_values = {}
    for item in update_params:
        if update_params[item] is not None and update_params[item] != '':
            update_values.update({item: update_params[item]})

    if update_values.get('passwd'):
        update_values['passwd'] = passwd_to_hash(update_values['passwd'])
    session = db.session()
    try:
        session.execute(update(User).where(User.id == user_id).values(**update_values))
        session.commit()
        user = get_user(user_id)
        auth.create_jwt_token(user)
        return user
    except sqlalchemy.exc.IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig)) from e


def delete_user(user_id: int, token: str) -> bool:
    """
    удаление юзера по ID
    :param token:
    :param user_id:
    :return: bool
    """
    user = auth.parse_jwt_token(token)
    if not get_user(user['id']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    if not get_user(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')

    if user['id'] != user_id and user['is_admin'] == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
    session = db.session()
    session.execute(update(User).where(User.id == user_id).values(state=False))
    session.commit()
    auth.remove_jwt_token(user_id)
    return True


def create_user(user: UserCreate) -> User:
    """
    Добавление нового пользователя
    :param user:
    :return: User
    """
    session = db.session()
    user_in_base = session.query(User).where(User.login == user.login, User.state == True).first()
    if user_in_base:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Login already used')
    try:
        new_user = User(login=user.login,
                        passwd=passwd_to_hash(user.passwd),
                        name=user.name,
                        city=user.city)
        session.add(new_user)
        session.commit()
        return new_user
    except sqlalchemy.exc.IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig)) from e


def passwd_to_hash(password: str) -> str:
    """
    Хэширование пароля
    :param password:
    :return: str
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def change_admin_role_to_user(new_admin: dict, token: str) -> bool:
    """
    Изменение прав пользователя
    :param new_admin:
    :param token:
    :return:
    """
    user = auth.parse_jwt_token(token)
    if not get_user(user['id']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    if user['id'] == new_admin['id']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You can`t change your role')

    session = db.session()
    session.execute(update(User).where(User.id == new_admin['id']).values(is_admin=new_admin['is_admin']))
    session.commit()
    return True


def user_login(user: UserLogin) -> str:
    """
    Функция логина, проверяет наличие юзера в базе и выдает токен авторизации
    :param user:
    :return: str
    """
    session = db.session()
    user.passwd = passwd_to_hash(user.passwd)
    user_in_base = session.query(User).where(User.login == user.login, User.state == True).first()
    if not user_in_base:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    if user_in_base.passwd != user.passwd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email or password invalid')
    access_token = auth.create_jwt_token(user_in_base)
    return json.dumps({"access_token": access_token, "admin": user_in_base.is_admin})


def user_logout(token: str) -> bool:
    """
    Выход пользователя, удаление токена
    :param token:
    :return: bool
    """
    user = auth.parse_jwt_token(token)
    if not get_user(user['id']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    auth.remove_jwt_token(user['id'])
    return True
