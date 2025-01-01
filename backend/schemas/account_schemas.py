from typing import Optional
from pydantic import BaseModel

from schemas.user_schemas import UserDetailsResponse


class AccountResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    currency: str
    user: Optional[UserDetailsResponse] = None

    class Config:
        orm_mode = True
        from_attributes = True

class CreateAccountRequest(BaseModel):
    user_id: int
    balance: float
    currency: str

class UpdateAccountRequest(BaseModel):
    balance: Optional[float] = None
    currency: Optional[str] = None