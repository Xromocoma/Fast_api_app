from fastapi import APIRouter, Response, status, Depends, Security

from app.core.dependencies import is_authentication, is_admin, security
from app.shemas.city import City
from app.core.city import city_add, city_update, city_delete, get_all_cities


router = APIRouter()


@router.get("/city",dependencies=[Depends(is_authentication), Security(security)])
def get_all_city():
    res = get_all_cities()
    if res:
        return res
    return []


@router.post("/city",
             dependencies=[Depends(is_authentication), Depends(is_admin), Security(security)])
def add_city(city: City):
    if city_add(city.name):
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/city/{city_id}",
            dependencies=[Depends(is_authentication), Depends(is_admin), Security(security)])
def update_city(city_id: int, city: City):
    res = city_update(city_id, city.dict())
    if res:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/city/{city_id}",
               dependencies=[Depends(is_authentication), Depends(is_admin), Security(security)])
def delete_city(city_id: int):
    res = city_delete(city_id)
    if res:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)
