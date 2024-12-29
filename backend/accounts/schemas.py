from pydantic import BaseModel

from auth.schemas import UserDetailsResponse
from cards.schemas import CardResponse
from transactions.schemas import TransactionResponse


class AccountResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    currency: str

    class Config:
        orm_mode = True
        from_attributes = True

class AccountOverviewResponse(BaseModel):
    user: UserDetailsResponse
    account: AccountResponse
    cards: list[CardResponse]
    transactions: list[TransactionResponse]