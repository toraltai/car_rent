from fastapi import APIRouter
from app.cars.urls import carRouter, carUtils


api_router = APIRouter()


api_router.include_router(carUtils, prefix='/utils', tags=['Utils'])
api_router.include_router(carRouter, prefix='/car', tags=['API for "Car" model'])