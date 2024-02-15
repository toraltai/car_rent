from fastapi import APIRouter
from app.cars.urls import carRouter


api_router = APIRouter()


api_router.include_router(carRouter, prefix='/car', tags=['cars'])