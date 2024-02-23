from tortoise import fields 
from tortoise.models import Model 
from dataclasses import dataclass
from tortoise.contrib.pydantic import pydantic_model_creator

from app.enums import *


class Category(Model):
    id: int
    title = fields.CharField(25)


@dataclass
class CreateCategory:
    title: str

GetCategory = pydantic_model_creator(Category, name='categories')


class Car(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(25)
    born = fields.CharField(25)
    volume = fields.CharField(25)
    gear = fields.CharField(25)
    engine = fields.CharField(25)
    transmission = fields.CharField(25)
    color = fields.CharField(25)
    price = fields.CharField(25)
    period = fields.CharEnumField(Period)
    category = fields.CharField(25)
    discount_price = fields.CharField(25)
    # user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
    #     "models.User", related_name="cars")

    @classmethod
    async def calculate(cls, price):
        calculated_price = price + "str"
        return calculated_price
    
    class Meta:
        table = "cars"

GetCar = pydantic_model_creator(Car, name="Car")
CreateCar = pydantic_model_creator(Car, name="CarIn", exclude_readonly=True, exclude=['discount_price'])

