from fastapi import APIRouter, Security, Response, status, Depends
from app.core.user import user_login, user_logout
from app.shemas.user import UserLogin
from app.core.dependencies import is_authentication, security
from fastapi.security import HTTPAuthorizationCredentials


router = APIRouter()


# Вход и получение токена авторизации
@router.post("/login",)
def login(user: UserLogin):
    login_ok = user_login(user)
    if not login_ok:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    return Response(login_ok, status_code=status.HTTP_200_OK)


# Выход и отчистка токена
@router.post("/logout",
             dependencies=[Depends(is_authentication)])
def logout(credentials: HTTPAuthorizationCredentials = Security(security)):
    user_logout(credentials.credentials)
    return Response(status_code=status.HTTP_200_OK)
