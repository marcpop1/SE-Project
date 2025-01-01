from pydantic import BaseModel

from schemas.account_schemas import AccountResponse
from schemas.user_schemas import UserDetailsResponse
from schemas.card_schemas import CardResponse
from schemas.transaction_schemas import TransactionResponse


class AccountOverviewResponse(BaseModel):
    user: UserDetailsResponse
    account: AccountResponse
    cards: list[CardResponse]
    transactions: list[TransactionResponse]