import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from auth.schemas import UserDetailsResponse
from auth.user_roles import UserRole
from database import SessionLocal
from fastapi import Request

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')


def get_db():
    with SessionLocal() as session:
        yield session

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated. Could not get cookie.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('id')
        username: str = payload.get('sub')
        name: str = payload.get('name')
        role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return UserDetailsResponse(
            id = user_id,
            username = username,
            name = name,
            role = role
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user. JWT Error.')

async def get_admin_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated. Could not get cookie.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('id')
        username: str = payload.get('sub')
        name: str = payload.get('name')
        role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        if role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='User is not admin.')
        return UserDetailsResponse(
            id = user_id,
            username = username,
            name = name,
            role = role
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user. JWT Error.')

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserDetailsResponse, Depends(get_current_user)]
admin_dependency = Annotated[UserDetailsResponse, Depends(get_admin_user)]
