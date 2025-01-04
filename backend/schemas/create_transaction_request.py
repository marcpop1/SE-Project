from pydantic import BaseModel


class CreateTransactionRequest(BaseModel):
    account_to_username: str
    amount: float
    currency: str