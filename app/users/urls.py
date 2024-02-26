from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

import jwt

from .models import User, CreateUser, GetUser, bcrypt
from .auth import authenticate_user, get_current_user
from config import settings


userRouter=APIRouter()


@userRouter.post('/register', response_model=GetUser)
async def create_user(user: CreateUser): #type: ignore
    user_obj = User(name=user.name,
                    role = 'partner',
                    password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await GetUser.from_tortoise_orm(user_obj)


@userRouter.post('/login', summary='Login')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password' )

    user_obj = await GetUser.from_tortoise_orm(user)
    token_payload = {'id': user_obj.id,}

    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
    context = {'access_token' : token, 'token_type' : 'bearer'}
    
    headers = {"Accept": "application/json",
               "Authorization": f"Bearer {token}"}

    response = JSONResponse(context, headers=headers)

    return response


@userRouter.get('/me', response_model=GetUser)
async def get_user(user: GetUser = Depends(get_current_user)): # type: ignore
    return user