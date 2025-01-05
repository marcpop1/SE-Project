from pydantic import BaseModel

from schemas.account_response import AccountResponse
from schemas.user_details_response import UserDetailsResponse
from schemas.card_response import CardResponse
from schemas.transaction_response import TransactionResponse


class AccountOverviewResponse(BaseModel):
    user: UserDetailsResponse
    account: AccountResponse
    cards: list[CardResponse]
    transactions: list[TransactionResponse]