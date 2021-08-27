import hashlib
import json
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import update

from app.shemas.user import UserCreate, UserLogin
from app.models import User
from app.core.database import db
from app.core.authorization import auth


def get_all_users() -> List[User]:
    """
    Получение списка всех юзеров
    :return: List[User]
    """
    session = db.session()
    users = session.query(User).where(User.state == True)
    result = []
    for user in users:
        result.append(user)
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


def update_user(user_id: int, user: dict) -> bool:
    """
    Обновить юзера по ID, обновляемые поля динамические.
    :param user_id:
    :param user:
    :return: bool
    """
    if not get_user(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    # создаем новый dict с НЕ пустыми значениями для апдейта
    update_values = {}
    for item in user:
        if user[item] is not None and user[item] != '':
            update_values.update({item: user[item]})

    if update_values.get('passwd'):
        update_values['passwd'] = passwd_to_hash(update_values['passwd'])

    session = db.session()
    session.execute(update(User).where(User.id == user_id).values(**update_values))
    session.commit()
    user = get_user(user_id)
    auth.create_jwt_token(user)
    return True


def delete_user(user_id: int, token: str) -> bool:
    """
    удаление юзера по ID
    :param token:
    :param user_id:
    :return: bool
    """
    if not get_user(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    user_data = auth.parse_jwt_token(token)
    if user_data['id'] == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You can`t delete yourself')
    session = db.session()
    session.execute(update(User).where(User.id == user_id).values(state=False))
    session.commit()
    return True


def create_user(user: UserCreate) -> User:
    """
    Добавление нового пользователя
    :param user:
    :return: User
    """
    session = db.session()
    user_in_base = session.query(User).where(User.email == user.email, User.state == True).first()
    if user_in_base:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already used')
    new_user = User(email=user.email,
                    passwd=passwd_to_hash(user.passwd),
                    name=user.name,
                    state=user.state,
                    is_admin=user.is_admin)
    session.add(new_user)
    session.commit()
    return new_user


def passwd_to_hash(password: str) -> str:
    """
    Хэширование пароля
    :param password:
    :return: str
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def user_login(user: UserLogin) -> str:
    """
    Функция логина, проверяет наличие юзера в базе и выдает токен авторизации
    :param user:
    :return: str
    """
    session = db.session()
    user.passwd = passwd_to_hash(user.passwd)
    user_in_base = session.query(User).where(User.email == user.email, User.state == True).first()
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
