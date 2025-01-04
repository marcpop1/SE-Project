from pydantic import BaseModel


class CardDetailResponse(BaseModel):
    id: int
    holder_name: str
    number: str
    expiration_month: int
    expiration_year: int
    cvv: int
    type: str
    currency: str

    class Config:
        from_attributes = True
        alias_generator = lambda string: ''.join(
            word.capitalize() if i else word
            for i, word in enumerate(string.split('_'))
        )
        populate_by_name = True


class CreateCardRequest(BaseModel):
    type: str
    currency: str


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

    class Config:
        orm_mode = True
        from_attributes = True
