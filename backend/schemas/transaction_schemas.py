from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from schemas.account_schemas import AccountResponse
from shared.enums.transaction.transaction_type import TransactionType

class TransactionResponse(BaseModel):
    id: int
    account_from_id: int
    account_to_id: int
    amount: float
    currency: str
    created_at: datetime
    account_from: Optional[AccountResponse] = None
    account_to: Optional[AccountResponse] = None
    status: int
    type: TransactionType
    class Config:
        from_attributes = True
        alias_generator = lambda string: ''.join(
            word.capitalize() if i else word
            for i, word in enumerate(string.split('_'))
        )
        populate_by_name = True

class CreateTransactionRequest(BaseModel):
    account_to_username: str
    amount: float
    currency: str

class AddMoneyRequest(BaseModel):
    amount: float

class UpdateTransactionRequest(BaseModel):
    account_from_id: Optional[int] = None
    account_to_id: Optional[int] = None
    amount: Optional[float] = None
    currency: Optional[str] = None