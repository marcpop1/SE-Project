from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from starlette import status

from dependencies import SECRET_KEY, ALGORITHM, get_auth_service
from models.user import User
from schemas.user_schemas import CreateUserRequest, Token

from fastapi_restful.cbv import cbv

from services.auth_service import AuthenticationService

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


COOKIE_TOKEN_KEY='access_token'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

@cbv(router)
class AuthenticationController:
    authentication_service: AuthenticationService = Depends(get_auth_service)
    
    @router.post("/register", status_code=201)
    async def register(self, payload: CreateUserRequest):
        self.authentication_service.register_user(data=payload, bcrypt=bcrypt_context)
        
    @router.post("/login", response_model=Token)
    async def login(self, response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        user = self.authentication_service.authenticate(
            username=form_data.username,
            password=form_data.password,
            bcrypt=bcrypt_context
        )
        
        token = self.authentication_service.create_access_token(
            user=user,
            key=SECRET_KEY,
            alg=ALGORITHM,
        )
        
        response.set_cookie(
            key=COOKIE_TOKEN_KEY,
            value=token,
            httponly=True,
            secure=True
        )
        
        return {'access_token': token, 'token_type': 'bearer'}
        
    @router.post('/logout', status_code=200)
    async def logout(self, response: Response):
        response.delete_cookie(key=COOKIE_TOKEN_KEY)
        return {'message': 'Successfully logged out'}
