from fastapi import APIRouter, Response, status
from app.shemas.publication import PublicationCreate,PublicationUpdate,PublicationDelete
from app.core.publications import get_all_publications,create_publication,delete_publication,update_publication
router = APIRouter()



@router.get("/publications")
def get_all():
    res = get_all_publications()
    if res:
        return res
    return []


@router.post("/publications")
def add_publication(params: PublicationCreate):
    res = create_publication(params.dict())
    if res:
        return res
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/publications/{publication_id}")
def change_publication(publication_id: int, params: PublicationUpdate):
    res = update_publication(publication_id, params.dict())
    if res:
        return res
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/publications/{publication_id}")
def del_publication(publication_id: int):
    if delete_publication(publication_id):
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)
