from pydantic import BaseModel


class CreateAccountRequest(BaseModel):
    user_id: int
    balance: float
    currency: str