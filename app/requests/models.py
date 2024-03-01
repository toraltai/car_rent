from tortoise import Tortoise, fields 
from tortoise.models import Model 
from dataclasses import dataclass
from tortoise.contrib.pydantic import pydantic_model_creator
from app.cars.models import Car


class Request(Model):
    id = fields.IntField(pk=True)
    # full_name = fields.CharField(128)
    region = fields.CharField(25)
    # telepnone = fields.CharField(13) # 13 - это длина номера вместе с +
    # field = fields.JSONField()
    car: fields.ForeignKeyRelation[Car] = fields.ForeignKeyField(
        "models.Car", related_name="cars", null=True)


Tortoise.init_models(["app.requests.models"], "models")
GetRequest = pydantic_model_creator(Request, name='Reqeust')
CreateRequest = pydantic_model_creator(Request, name="RequestIn", exclude_readonly=True, exclude=['car_id'])


# TODO Проверить пути на скорость и лишние запросы.