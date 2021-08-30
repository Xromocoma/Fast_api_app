from fastapi import APIRouter, Response, status, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials

from app.core.dependencies import is_authentication, security
from app.shemas.publication import PublicationCreate, PublicationUpdate
from app.core.publications import get_all_publications, create_publication, delete_publication, update_publication

router = APIRouter()


@router.get("/publications",
            dependencies=[Depends(is_authentication), Security(security)])
def get_all(sort: int = None, find_str: str = None, city: int = None, user: int = None):
    res = get_all_publications(sort=sort, search_string=find_str, city=city, user=user)
    if res:
        return res
    return []


@router.post("/publications",
             dependencies=[Depends(is_authentication), Security(security)])
def add_publication(params: PublicationCreate, credentials: HTTPAuthorizationCredentials = Security(security)):
    res = create_publication(params.dict(), credentials.credentials)
    if res:
        return res
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/publications/{publication_id}",
            dependencies=[Depends(is_authentication), Security(security)])
def change_publication(publication_id: int,
                       params: PublicationUpdate,
                       credentials: HTTPAuthorizationCredentials = Security(security)):
    res = update_publication(publication_id, params.dict(), credentials.credentials)

    if res:
        return res
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/publications/{publication_id}",dependencies=[Depends(is_authentication), Security(security)])
def del_publication(publication_id: int, credentials: HTTPAuthorizationCredentials = Security(security)):
    if delete_publication(publication_id, credentials.credentials):
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)
