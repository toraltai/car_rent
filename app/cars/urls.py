from fastapi import APIRouter
from typing import List
from .models import Car, GetCar, CreateCar, GetCategory


carRouter = APIRouter()


# @carRouter.post('/')
# async def create_category(cat_obj: CreateCategory):
#     category_obj = await Category.create(title = cat_obj.title)
#     return {"id":category_obj.id, "title":category_obj.title}


@carRouter.post('/cr', response_model=GetCar, description="Api for add car")
async def create_car(car: CreateCar):
    price = car.price + 'str'
    car_obj = await Car.create(**car.dict(exclude_unset=True),
                               discount_price = price)
    return await GetCar.from_tortoise_orm(car_obj)


@carRouter.get('/car_list', response_model=List[GetCar])
async def get_car():
    return await GetCar.from_queryset(Car.all())