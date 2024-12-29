from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TransactionResponse(BaseModel):
    id: int
    account_from_id: int
    account_to_id: int
    amount: float
    currency: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class CreateTransactionRequest(BaseModel):
    account_from_id: int
    account_to_id: int
    amount: float
    currency: str
    created_at: Optional[datetime] = None

class UpdateTransactionRequest(BaseModel):
    account_from_id: Optional[int] = None
    account_to_id: Optional[int] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    created_at: Optional[datetime] = None