from pydantic import BaseModel
from datetime import datetime

class TransactionResponse(BaseModel):
    id: int
    account_from_id: int
    account_to_id: int
    amount: float
    currency: str
    datetime: datetime

    class Config:
        orm_mode = True
        from_attributes = True