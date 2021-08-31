import jwt
from app.config import settings
from app.core.redis import Redis
from app.shemas.user import UserFullData


class Auth(Redis):
    """
    Класс авторизации
    """
    def set_jwt_token(self, user_id: int, payload: str) -> None:
        """
        Установка Jwt токена в редис по ID
        :param user_id:
        :param payload:
        :return: None
        """
        self.set(name=f'Access_{user_id}',
                 value=payload)

    def get_jwt_token(self, user_id: int)-> str or None:
        """
        Получение Jwt токена по ID
        :param user_id:
        :return: str or None
        """
        res = self.get(f'Access_{user_id}')
        if res:
            return res.decode('UTF-8')
        return None

    def remove_jwt_token(self, user_id: int) -> None:
        """
        Удаление Jwt токена по ID
        :param user_id:
        :return: None
        """
        self.remove(f'Access_{user_id}')

    def check_jwt_token(self, user_id: int, token: str) -> bool:
        """
        Проверка Jwt токена на совпадение и наличие в базе
        :param user_id:
        :param token:
        :return:
        """
        token_from_redis = self.get_jwt_token(user_id)
        if token_from_redis:
            if token == token_from_redis:
                return True
        return False

    def create_jwt_token(self, user: UserFullData) -> str:
        """
        Создание Jwt токена
        :param user:
        :return: str
        """
        user_payload = {
            "id": user.id,
            "login": user.login,
            "state": user.state,
            "is_admin": user.is_admin
        }
        payload = jwt.encode(user_payload, settings.JWT_KEY, algorithm='HS256')
        self.set_jwt_token(user_id=user.id,
                           payload=payload)
        return self.get_jwt_token(user.id)

    def parse_jwt_token(self, token: str) -> dict:
        """
        Расшифровка хэша
        :param token:
        :return: dict
        """
        return jwt.decode(token, settings.JWT_KEY, algorithms=['HS256'])

    def is_auth(self, token: str)-> bool:
        """
        Проверка токена на корректность
        :param token:
        :return: bool
        """
        user = self.parse_jwt_token(token)
        return self.check_jwt_token(user['id'], token)

    def is_admin(self, token: str) -> bool:
        """
        Проверка юзера(по токену) на права администратора
        :param token:
        :return:
        """
        user = self.parse_jwt_token(token)
        return user['is_admin']


auth = Auth()
