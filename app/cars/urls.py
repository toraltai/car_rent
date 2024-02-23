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
    price = await Car.calculate(car.price)
    car_obj = await Car.create(**car.dict(exclude_unset=True),
                               discount_price = price)
    return await GetCar.from_tortoise_orm(car_obj)


@carRouter.get('/car_list', response_model=List[GetCar])
async def get_car():
    return await GetCar.from_queryset(Car.all())


@carRouter.get('/car/{car_id}', response_model=GetCar)
async def car_get_by_id(car_id):
    return await GetCar.from_queryset_single(Car.get(id=car_id))


@carRouter.put('/car/{car_id}', response_model=GetCar)
async def car_get_by_id(car_id):
    await Car.filter(id=car_id).update(**car_id.model_dump(exclude_unset=True))
    return await Car.from_queryset_single(Car.get(id=car_id))

