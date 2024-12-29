from pydantic import BaseModel


class CardDetailResponse(BaseModel):
    id: int
    holder_name: str
    number: str
    expiration_month: int
    expiration_year: int
    type: str
    currency: str
    is_primary: bool

    class Config:
        orm_mode = True
        from_attributes = True


class CreateCardRequest(BaseModel):
    account_id: int
    card_type: str
    card_currency: str
    is_primary: bool


class CardResponse(BaseModel):
    id: int
    account_id: int
    holder_name: str
    number: str
    expiration_month: int
    expiration_year: int
    cvv: str
    type: str
    currency: str
    is_primary: bool

    class Config:
        orm_mode = True
        from_attributes = True