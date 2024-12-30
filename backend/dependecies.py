import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from accounts.repositories import AccountRepository
from auth.schemas import UserDetailsResponse
from cards.repositories import CardRepository
from cards.services import CardService
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
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return UserDetailsResponse(
            id=user_id,
            username=username
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user. JWT Error.')


# repositories
def get_card_repository(db: Session = Depends(get_db)) -> CardRepository:
    return CardRepository(session=db)


def get_account_repository(db: Session = Depends(get_db)) -> AccountRepository:
    return AccountRepository(session=db)


# services
def get_card_service(
        card_repository: CardRepository = Depends(get_card_repository),
        account_repository: AccountRepository = Depends(get_account_repository)
) -> CardService:
    return CardService(card_repository, account_repository)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserDetailsResponse, Depends(get_current_user)]

# renamed dependencies

DbSession = Annotated[Session, Depends(get_db)]
LoggedUser = Annotated[UserDetailsResponse, Depends(get_current_user)]
