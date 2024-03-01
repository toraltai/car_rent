from fastapi import APIRouter
from app.cars.urls import carRouter, carUtils
from app.users.urls import userRouter
from app.requests.urls import requestRouter


api_router = APIRouter()


api_router.include_router(userRouter, prefix='/users', tags=['API for USERS'])
api_router.include_router(carUtils, prefix='/utils', tags=['Utils'])
api_router.include_router(carRouter, prefix='/cars', tags=['API for "Car" model'])
api_router.include_router(requestRouter, prefix='/requests', tags=['API for send requests'])