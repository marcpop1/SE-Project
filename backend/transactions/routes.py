from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from transactions.transaction_repository import TransactionRepository
from transactions.models import Transaction
from .schemas import TransactionResponse, CreateTransactionRequest, UpdateTransactionRequest
from dependencies import db_dependency, user_dependency

router = APIRouter(
    prefix='/transactions',
    tags=['transactions']
)

def get_transaction_repository(db: db_dependency) -> TransactionRepository:
    return TransactionRepository(db)

repository_dependency = Annotated[TransactionRepository, Depends(get_transaction_repository)]

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create(transaction: CreateTransactionRequest, user: user_dependency, repository: repository_dependency):
    new_transaction = Transaction(**transaction.dict())
    return repository.add(new_transaction)

@router.get("/", response_model=List[TransactionResponse])
def get_all(user: user_dependency, repository: repository_dependency):
    return repository.get_all(user.id)

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_by_id(transaction_id: int, user: user_dependency, repository: repository_dependency):
    transaction = repository.get_by_id(transaction_id, user.id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update(transaction_id: int, transaction: UpdateTransactionRequest, user: user_dependency, repository: repository_dependency):
    existing_transaction = repository.get_by_id(transaction_id, user.id)
    if existing_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in transaction.dict().items():
        setattr(existing_transaction, key, value)
    return repository.update(existing_transaction)

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(transaction_id: int, user: user_dependency, repository: repository_dependency):
    transaction = repository.get_by_id(transaction_id, user.id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    repository.delete(transaction)
    return None