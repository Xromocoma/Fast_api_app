from fastapi import APIRouter, Response, status
from app.shemas.city import City
from app.core.city import city_add, city_update, city_delete, get_all_cities


router = APIRouter()


@router.get("/city")
def get_all_city():
    res = get_all_cities()
    if res:
        return res
    return []


@router.post("/city")
def add_city(city: City):
    if city_add(city.name):
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/city/{city_id}")
def update_city(city_id: int, city: City):
    res = city_update(city_id, city.dict())
    if res:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/city/{city_id}")
def delete_city(city_id: int):
    res = city_delete(city_id)
    if res:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_400_BAD_REQUEST)
