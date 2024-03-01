from fastapi import APIRouter
from .models import Request, GetRequest, CreateRequest
from typing import List, Optional
from app.cars.models import Car
from tortoise.query_utils import Prefetch


requestRouter = APIRouter()


@requestRouter.post('/', response_model=GetRequest)
async def post(obj: CreateRequest, car_id: Optional[int] = None): #type: ignore
    request_obj = await Request.create(**obj.dict(exclude_unset=True),
                                       car_id = car_id)
    return await GetRequest.from_tortoise_orm(request_obj)


@requestRouter.get('/all', response_model=List[GetRequest])
async def get():
    return await GetRequest.from_queryset(Request.all().prefetch_related('car'))