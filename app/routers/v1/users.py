from typing import List
from fastapi import status, Response, Depends, Security, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.core.user import get_all_users, get_user, update_user, delete_user, create_user
from app.shemas.user import UserCreate, UserUpdate, UserInfo
from app.core.dependencies import is_authentication, security, is_admin


router = APIRouter()


# Получение списка всех юзеров по UID
@router.get("/users",
            response_model=List[UserInfo],
            dependencies=[Depends(is_authentication), Security(security)])
def get_users():
    return get_all_users()


# Получение юзера по UID
@router.get("/users/{user_id}",
            response_model=UserInfo,
            dependencies=[Depends(is_authentication), Security(security)])
def get_user_by_id(user_id: int):

    return get_user(user_id)


# Обновление юзера по UID, поля динамические
@router.put("/users/{user_id}",
            dependencies=[Depends(is_authentication), Depends(is_admin), Security(security)])
def user_update(user_id: int, user_data: UserUpdate):
    if update_user(user_id, user_data.dict()):
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


# Удаление юзера по UID
@router.delete("/users/{user_id}",
               dependencies=[Depends(is_authentication), Depends(is_admin), Security(security)])
def user_del(user_id: int, credentials: HTTPAuthorizationCredentials = Security(security)):
    if delete_user(user_id, credentials.credentials):
        return Response(status_code=status.HTTP_200_OK)


# Добавление юзера
@router.post("/users/create",
             dependencies=[Depends(is_authentication), Depends(is_admin), Security(security)])
async def user_create(user_data: UserCreate):
    if create_user(user_data):
        return Response(status_code=status.HTTP_200_OK)


