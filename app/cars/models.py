from tortoise import Tortoise, fields 
from tortoise.models import Model 
from dataclasses import dataclass
from tortoise.contrib.pydantic import pydantic_model_creator

from app.users.models import User
from app.enums import *


class Category(Model):
    id: int
    title = fields.CharField(25)

@dataclass
class CreateCategory:
    title: str

GetCategory = pydantic_model_creator(Category)


class Color(Model):
    id: int
    title = fields.CharField(25)

@dataclass
class CreateColor:
    title: str

GetColor = pydantic_model_creator(Color)


class Car(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(25)
    born = fields.DateField()
    volume = fields.CharField(25)
    gear = fields.CharField(25)
    engine = fields.CharField(25)
    transmission = fields.CharField(25)
    color: fields.ForeignKeyRelation[Color] = fields.ForeignKeyField(
        "models.Color", related_name="cars")
    price = fields.CharField(25)
    period = fields.CharEnumField(Period)
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        "models.Category", related_name="cars")
    discount_price = fields.CharField(25)
    company: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="cars")

    @classmethod
    async def calculate(cls, price):
        calculated_price = price + "str"
        return calculated_price
    
    class Meta:
        table = "cars"

Tortoise.init_models(["app.cars.models"], "models")
GetCar = pydantic_model_creator(Car, name="Car")
CreateCar = pydantic_model_creator(Car, name="CarIn", exclude_readonly=True, exclude=['discount_price'])

