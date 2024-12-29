from pydantic import BaseModel


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
