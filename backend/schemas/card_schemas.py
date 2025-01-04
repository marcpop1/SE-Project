from pydantic import BaseModel


class CardResponse(BaseModel):
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