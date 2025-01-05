from pydantic import BaseModel


class CreateCardRequest(BaseModel):
    type: str
    currency: str