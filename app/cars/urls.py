from fastapi import APIRouter, HTTPException, Response
from typing import List
from pydantic import BaseModel
# from .models import Car, GetCar, CreateCar, GetCategory
from .models import *


carRouter = APIRouter()
carUtils = APIRouter()


class Status(BaseModel):
    message: str


# EndPoints for Category
@carUtils.post('/category')
async def create_category(cat_obj: CreateCategory):
    category_obj = await Category.create(title = cat_obj.title)
    return {"id":category_obj.id, "title":category_obj.title}

@carUtils.get('/category', response_model=GetCategory, summary="Single object")
async def get(obj_id: int):
    return await GetCategory.from_queryset_single(Category.get(id=obj_id))

@carUtils.put('/category/{cat_id}', response_model=GetCategory, description='Изменение по айди')
async def put_by_id(cat_id: int, obj: CreateCategory):
    await Category.get(id=cat_id).update(**obj.model_dump(exclude_unset=True))
    return await GetCategory.from_queryset_single(Color.get(id=cat_id))

@carUtils.delete('/category')
async def remove(cat_obj: int):
    category = await Category.get_or_none(id=cat_obj)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category {cat_obj} not found")
    await category.delete()
    return Status(message=f"Deleted category {category.title}")


# EndPoints for Color
@carUtils.post('/color')
async def post(object_: CreateColor):
    color_obj = await Color.create(title = object_.title)
    return {"id":color_obj.id, "title":color_obj.title}

@carUtils.get('/color', response_model=GetColor, summary="Single object")
async def get(obj_id: int):
    return await GetColor.from_queryset_single(Color.get(id=obj_id))

@carUtils.put('/color/{color_id}', response_model=GetColor, description='Изменение по айди')
async def put_by_id(color_id: int, obj: CreateColor):
    await Color.get(id=color_id).update(**obj.model_dump(exclude_unset=True))
    return await GetColor.from_queryset_single(Color.get(id=color_id))

@carUtils.delete('/color')
async def remove(object_: int):
    deleted_count = await Color.filter(id=object_).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {object_} not found")
    return Status(message=f"Deleted user {object_}")


# EndPoints for Car(CRUD)
@carRouter.post('/', response_model=GetCar, description="Api for add car")
async def create_car(car: CreateCar):
    price = await Car.calculate(car.price)
    car_obj = await Car.create(**car.dict(exclude_unset=True),
                               discount_price = price)
    return await GetCar.from_tortoise_orm(car_obj)

@carRouter.get('/{car_id}', response_model=GetCar,description='Получение по айди')
async def get_car_by_id(car_id):
    return await GetCar.from_queryset_single(Car.get(id=car_id))

@carRouter.put('/{car_id}', response_model=GetCar, description='Изменения по айди')
async def put_car_by_id(car_id: int, car_obj: CreateCar):
    await Car.get(id=car_id).update(**car_obj.model_dump(exclude_unset=True))
    return await GetCar.from_queryset_single(Car.get(id=car_id))

@carRouter.get('/list', response_model=List[GetCar], description='Список всех машин')
async def get_car():
    return await GetCar.from_queryset(Car.all())