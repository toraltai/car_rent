from fastapi import APIRouter
from app.cars.urls import carRouter, carUtils
from app.users.urls import userRouter


api_router = APIRouter()


api_router.include_router(userRouter, prefix='/user', tags=['API for USERS'])
api_router.include_router(carUtils, prefix='/utils', tags=['Utils'])
api_router.include_router(carRouter, prefix='/car', tags=['API for "Car" model'])