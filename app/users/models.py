from tortoise import Tortoise, fields 
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from ..enums import Role

from passlib.hash import bcrypt


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    password_hash = fields.CharField(128)
    role = fields.CharEnumField(Role, max_length=15)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)
    
    class Meta:
        table = 'users'

GetUser = pydantic_model_creator(User, name='User', exclude=['password_hash'])
CreateUser = pydantic_model_creator(User, name='UserIn', exclude_readonly=True, exclude=['role'])