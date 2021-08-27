from fastapi.security import HTTPBearer
from fastapi import Request
from fastapi import HTTPException, status

from app.core.authorization import auth


security = HTTPBearer()


async def is_authentication(request: Request) -> None:
    """
    Проверка на авторизацию пользователя(по токену), вспомонательная функция (Depends)
    :param request:
    :return: None
    """
    access_token = request.headers.get('Authorization')
    if access_token and access_token:
        access_token = access_token.split()[1]
        if access_token == "null":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you haven`t Authorization")
        is_auth = auth.is_auth(token=access_token)
        if not is_auth:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you haven`t Authorization")


async def is_admin(request: Request) -> None:
    """
    Проверка на права админа у пользователя(по токену), вспомонательная функция (Depends)
    :param request:
    :return: None
    """
    access_token = request.headers.get('Authorization')
    if access_token:
        access_token = access_token.split()[1]
        if access_token == "null":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you haven`t Authorization")
        admin = auth.is_admin(token=access_token)
        if not admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
