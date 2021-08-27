
from fastapi import APIRouter
from app.routers.v1 import city, users, publication, auth

api_router = APIRouter()
api_router.include_router(city.router, tags=["city"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(publication.router, tags=["publication"])
api_router.include_router(auth.router, tags=["auth"])
