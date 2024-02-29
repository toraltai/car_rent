from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config.settings import SECRET_KEY
from app.users.models import User, GetUser
import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/users/login')


async def authenticate_user(username: str, password: str):
    user = await User.get(name=username)
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user 


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    user = await User.filter(id=payload.get('id')).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return await GetUser.from_tortoise_orm(user)