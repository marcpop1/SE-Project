from pydantic import BaseModel

from accounts.schemas import AccountResponse
from auth.schemas import UserDetailsResponse
from cards.schemas import CardResponse
from transactions.schemas import TransactionResponse


class AccountOverviewResponse(BaseModel):
    user: UserDetailsResponse
    account: AccountResponse
    cards: list[CardResponse]
    transactions: list[TransactionResponse]