import os
from typing import Annotated

from controllers.transaction_serializer_controller import TransactionSerializerController
from controllers.account_overview_controller import AccountOverviewController
from views.currency_view import CurrencyView
from repositories.account_repository import AccountRepository
from repositories.card_repository import CardRepository
from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from controllers.account_controller import AccountController
from controllers.user_controller import UserController
from controllers.card_controller import CardController
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from schemas.user_details_response import UserDetailsResponse
from controllers.transaction_controller import TransactionController
from controllers.user_controller import UserController
from shared.enums.user.user_role import UserRole
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

# repositories
def get_card_repository(db: Session = Depends(get_db)) -> CardRepository:
    return CardRepository(session=db)

def get_account_repository(db: Session = Depends(get_db)) -> AccountRepository:
    return AccountRepository(session=db)

def get_transaction_repository(db: Session = Depends(get_db)) -> TransactionRepository:
    return TransactionRepository(session=db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(session=db)

# views
def get_currency_view() -> CurrencyView:
    return CurrencyView()

# controllers
def get_transaction_serializer() -> TransactionSerializerController:
    return TransactionSerializerController()

def get_card_controller(
        card_repository: CardRepository = Depends(get_card_repository),
        account_repository: AccountRepository = Depends(get_account_repository)
) -> CardController:
    return CardController(card_repository, account_repository)

def get_account_controller(
    account_repository: AccountRepository = Depends(get_account_repository)
) -> AccountController:
    return AccountController(account_repository)

def get_transaction_controller(
    account_repository: AccountRepository = Depends(get_account_repository),
    transaction_repository: TransactionRepository = Depends(get_transaction_repository),
    transaction_serializer: TransactionSerializerController = Depends(get_transaction_serializer),
    currency_controller: CurrencyView = Depends(get_currency_view)
) -> TransactionController:
    return TransactionController(account_repository, transaction_repository, transaction_serializer, currency_controller)

def get_user_controller(
    user_repository: UserRepository = Depends(get_user_repository),
    account_repository: AccountRepository = Depends(get_account_repository)
) -> UserController:
    return UserController(user_repository, account_repository)

def get_account_overview_controller(
    user: UserDetailsResponse = Depends(get_current_user),
    account_repository: AccountRepository = Depends(get_account_repository),
    transaction_repository: TransactionRepository = Depends(get_transaction_repository),
    card_repository: CardRepository = Depends(get_card_repository),
    transaction_serializer: TransactionSerializerController = Depends(get_transaction_serializer)
) -> AccountOverviewController:
    return AccountOverviewController(user, account_repository, transaction_repository, card_repository, transaction_serializer)

DbSession = Annotated[Session, Depends(get_db)]
LoggedUser = Annotated[UserDetailsResponse, Depends(get_current_user)]