import os
from typing import Annotated

from services.transaction_serializer_service import TransactionSerializerService
from services.account_overview_service import AccountOverviewService
from controllers.currency_controller import CurrencyController
from repositories.account_repository import AccountRepository
from repositories.card_repository import CardRepository
from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository
from services.account_service import AccountService
from services.auth_service import AuthenticationService
from services.card_service import CardService
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from schemas.user_schemas import UserDetailsResponse
from services.transaction_service import TransactionService
from services.user_service import UserService
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

# controllers
def get_currency_controller() -> CurrencyController:
    return CurrencyController()

# services
def get_transaction_serializer() -> TransactionSerializerService:
    return TransactionSerializerService()

def get_card_service(
        card_repository: CardRepository = Depends(get_card_repository),
        account_repository: AccountRepository = Depends(get_account_repository)
) -> CardService:
    return CardService(card_repository, account_repository)

def get_account_service(
    account_repository: AccountRepository = Depends(get_account_repository)
) -> AccountService:
    return AccountService(account_repository)

def get_transaction_service(
    account_repository: AccountRepository = Depends(get_account_repository),
    transaction_repository: TransactionRepository = Depends(get_transaction_repository),
    transaction_serializer: TransactionSerializerService = Depends(get_transaction_serializer),
    currency_controller: CurrencyController = Depends(get_currency_controller)
) -> TransactionService:
    return TransactionService(account_repository, transaction_repository, transaction_serializer, currency_controller)

def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    account_repository: AccountRepository = Depends(get_account_repository)
) -> AuthenticationService:
    return AuthenticationService(user_repository, account_repository)

def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository)

def get_account_overview_service(
    user: UserDetailsResponse = Depends(get_current_user),
    account_repository: AccountRepository = Depends(get_account_repository),
    transaction_repository: TransactionRepository = Depends(get_transaction_repository),
    card_repository: CardRepository = Depends(get_card_repository),
    transaction_serializer: TransactionSerializerService = Depends(get_transaction_serializer)
) -> AccountOverviewService:
    return AccountOverviewService(user, account_repository, transaction_repository, card_repository, transaction_serializer)

DbSession = Annotated[Session, Depends(get_db)]
LoggedUser = Annotated[UserDetailsResponse, Depends(get_current_user)]