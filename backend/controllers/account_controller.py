from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from repositories.account_repository import AccountRepository
from models.account import Account
from schemas.account_schemas import AccountResponse, CreateAccountRequest, UpdateAccountRequest
from dependencies import get_db, user_dependency

router = APIRouter(
    prefix='/accounts',
    tags=['accounts']
)

def get_account_repository(db: Session = Depends(get_db)) -> AccountRepository:
    return AccountRepository(db)

@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account: CreateAccountRequest, repository: AccountRepository = Depends(get_account_repository)):
    new_account = Account(**account.dict())
    return repository.add(new_account)

@router.get("/", response_model=List[AccountResponse])
def read_accounts(user: user_dependency, repository: AccountRepository = Depends(get_account_repository)):
    return repository.get_all(user.id)

@router.get("/{account_id}", response_model=AccountResponse)
def read_account(account_id: int, repository: AccountRepository = Depends(get_account_repository)):
    account = repository.get_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/user/", response_model=AccountResponse)
def read_account_by_user_id(user: user_dependency, repository: AccountRepository = Depends(get_account_repository)):
    account = repository.get_by_user_id(user.id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/username/{username}", response_model=AccountResponse)
def read_account_by_username(username: str, repository: AccountRepository = Depends(get_account_repository)):
    account = repository.get_by_username(username)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, account: UpdateAccountRequest, repository: AccountRepository = Depends(get_account_repository)):
    existing_account = repository.get_by_id(account_id)
    if existing_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    for key, value in account.dict().items():
        setattr(existing_account, key, value)
    return repository.update(existing_account)

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, repository: AccountRepository = Depends(get_account_repository)):
    account = repository.get_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    repository.delete(account)
    return None