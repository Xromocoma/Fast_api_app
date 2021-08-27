from fastapi import HTTPException, status
import redis

from app.config import settings


class Redis:
    """
    Класс для работы с редисом
    """

    def __init__(self):
        self.instance = redis.Redis(host=settings.REDIS_HOST,
                                    port=settings.REDIS_PORT)

    def set(self, name: str, value: str) -> None:
        """
        Запись в Redis
        :param name:
        :param value:
        :return: None
        """
        res = self.instance.set(name=name,
                                value=value,
                                keepttl=settings.REDIS_TTL)
        if not res:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Redis can`t save data")

    def get(self, name: str)->str:
        """
        Чтение из Redis
        :param name:
        :return:
        """
        return self.instance.get(name)

    def remove(self, name: str)-> None:
        """
        Удаление записи в Redis
        :param name:
        :return:
        """
        self.instance.delete(name)
