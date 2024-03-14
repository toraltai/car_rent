from fastapi import APIRouter, HTTPException, Depends, Response
from typing import List, Annotated
from pydantic import BaseModel
from app.users.auth import get_current_user
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

@carUtils.get('/category/all', response_model=List[GetCategory])
async def all_list():
    return await GetCategory.from_queryset(Category.all())

@carUtils.get('/category/{cat_id}', response_model=GetCategory, summary="Single object")
async def get(obj_id: int):
    return await GetCategory.from_queryset_single(Category.get(id=obj_id))

@carUtils.put('/category/{cat_id}', response_model=GetCategory, description='Изменение по айди')
async def put_by_id(cat_id: int, obj: CreateCategory):
    await Category.get(id=cat_id).update(title=obj.title)
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

@carUtils.get('/color/all', response_model=List[GetColor])
async def all_list():
    return await GetColor.from_queryset(Color.all())

@carUtils.get('/color', response_model=GetColor, summary="Single object")
async def get(obj_id: int):
    return await GetColor.from_queryset_single(Color.get(id=obj_id))

@carUtils.put('/color/{color_id}', response_model=GetColor, description='Изменение по айди')
async def put_by_id(color_id: int, obj: CreateColor):
    await Color.get(id=color_id).update(title=obj.title)
    return await GetColor.from_queryset_single(Color.get(id=color_id))

@carUtils.delete('/color')
async def remove(object_: int):
    deleted_count = await Color.filter(id=object_).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {object_} not found")
    return Status(message=f"Deleted user {object_}")


# EndPoints for Car(CRUD)
@carRouter.post('/', response_model=GetCar, summary="Api for add car")
async def create_car(car: CreateCar, current_user: Annotated[User, Depends(get_current_user)]): #type: ignore
    price = await Car.calculate(car.price)
    car_obj = await Car.create(**car.dict(exclude_unset=True),
                               discount_price = price,
                               company_id = current_user.id)
    return await GetCar.from_tortoise_orm(car_obj)

@carRouter.get('/obj/{car_id}', response_model=GetCar, summary='Получение по айди')
async def get_car_by_id(car_id):
    return await GetCar.from_queryset_single(Car.filter(id=car_id)
                                             .select_related('category','color','company').get())

@carRouter.put('/obj/{car_id}', response_model=GetCar, summary='Изменения по айди')
async def put_car_by_id(car_id: int, car_obj: CreateCar, current_user: Annotated[User, Depends(get_current_user)]): #type: ignore
    await Car.get(id=car_id).update(**car_obj.model_dump(exclude_unset=True))
    return await GetCar.from_queryset_single(Car.get(id=car_id))

@carRouter.get('/sort/{category_id}', response_model=List[GetCar], summary='Фильтрация по категориям')
async def all_list(category_id: int):
    return await GetCar.from_queryset(Car.filter(category_id=category_id)
                                       .select_related('category', 'color', 'company'))

@carRouter.get('/sort/{company_id}', response_model=List[GetCar], summary='Фильтрация по компаниям')
async def all_list(company_id: int):
    return await GetCar.from_queryset(Car.filter(company_id=company_id)
                                       .select_related('category', 'color', 'company'))

@carRouter.get('/list', response_model=List[GetCar], summary='Список данной компании')
async def all_list(current_company: Annotated[User, Depends(get_current_user)]):
    return await GetCar.from_queryset(Car.filter(company_id=current_company.id)
                                       .select_related('category', 'color', 'company'))

@carRouter.get('/all', response_model=List[GetCar])
async def get():
    return await GetCar.from_queryset(Car.all()
                                      .select_related('category', 'color', 'company'))

@carRouter.delete('/obj')
async def remove(object_: int):
    car_object = await Car.get_or_none(id=object_)
    if not car_object:
        raise HTTPException(status_code=404, detail=f"Something wrong")
    return Status(message=f"Car {car_object.title} was deleted")
# from tortoise import connections
# @carRouter.get('/all')
# async def all_list():
#     # return await GetCar.from_queryset(Car.all().prefetch_related('category'))
#     conn = connections.get('default')
#     return await conn.execute_query_dict("select * from cars")