from pydantic import BaseModel

from utils import snake_to_camel


class CardDetailResponse(BaseModel):
    id: int
    card_holder_name: str
    card_number: str
    expiration_month: int
    expiration_year: int
    card_type: str
    card_currency: str
    is_primary: bool

    class Config:
        from_attributes = True
        alias_generator = snake_to_camel


class CreateCardRequest(BaseModel):
    account_id: int
    card_type: str
    card_currency: str
    is_primary: bool
