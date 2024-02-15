from fastapi import APIRouter
from typing import List
from .models import *


carRouter = APIRouter()


@carRouter.post('/')
async def create_category(cat_obj: CreateCategory):
    category_obj = await Category.create(title = cat_obj.title)
    return {"id":category_obj.id, "title":category_obj.title}


@carRouter.get('/')
async def get_car():
    pass