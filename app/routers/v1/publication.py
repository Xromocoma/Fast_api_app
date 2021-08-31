from typing import List
from fastapi import APIRouter, Response, status, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from app.core.dependencies import is_authentication, security
from app.shemas.publication import PublicationCreate, PublicationUpdate, PublicationInfo
from app.core.publications import get_all_publications, create_publication, delete_publication, update_publication

router = APIRouter()


# Получение всех объявлений, фильтры опционально
@router.get("/publications",
            response_model=List[PublicationInfo],
            dependencies=[Depends(is_authentication), Security(security)])
def get_all(sort: int = None, find_string: str = None, city: int = None, users: int = None):
    res = get_all_publications(sort=sort, search_string=find_string, city=city, user=users)
    print(res)
    if res:
        return res
    return []


# Добавление объявлений
@router.post("/publications",
             response_model=PublicationInfo,
             dependencies=[Depends(is_authentication), Security(security)])
def add_publication(params: PublicationCreate, credentials: HTTPAuthorizationCredentials = Security(security)):
    res = create_publication(params.dict(), credentials.credentials)
    if res:
        return res
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


# Изменение объявлений
@router.put("/publications/{publication_id}",
            response_model=PublicationInfo,
            dependencies=[Depends(is_authentication), Security(security)])
def change_publication(publication_id: int,
                       params: PublicationUpdate,
                       credentials: HTTPAuthorizationCredentials = Security(security)):
    res = update_publication(publication_id, params.dict(), credentials.credentials)

    if res:
        return res
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


# Удаление объявлений
@router.delete("/publications/{publication_id}",
               dependencies=[Depends(is_authentication), Security(security)])
def del_publication(publication_id: int, credentials: HTTPAuthorizationCredentials = Security(security)):
    if delete_publication(publication_id, credentials.credentials):
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)
