from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from dependencies import SECRET_KEY, ALGORITHM, get_user_controller
from schemas.create_user_request import CreateUserRequest
from fastapi_restful.cbv import cbv
from controllers.user_controller import UserController
from schemas.token_response import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


COOKIE_TOKEN_KEY = "access_token"


@cbv(router)
class UserView:
    user_controller: UserController = Depends(get_user_controller)
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

    @router.post("/register", status_code=201)
    async def register(self, payload: CreateUserRequest):
        self.user_controller.register_user(data=payload, bcrypt=self.bcrypt_context)

    @router.post("/login", response_model=TokenResponse)
    async def login(
        self,
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ):
        user = self.user_controller.authenticate(
            username=form_data.username,
            password=form_data.password,
            bcrypt=self.bcrypt_context,
        )

        token = self.user_controller.create_access_token(
            user=user,
            key=SECRET_KEY,
            alg=ALGORITHM,
        )

        response.set_cookie(
            key=COOKIE_TOKEN_KEY, value=token, httponly=True, secure=True
        )

        return {COOKIE_TOKEN_KEY: token, "token_type": "bearer", "user_role": user.role}

    @router.post("/logout", status_code=200)
    async def logout(self, response: Response):
        response.delete_cookie(key=COOKIE_TOKEN_KEY)
        return {"message": "Successfully logged out"}
