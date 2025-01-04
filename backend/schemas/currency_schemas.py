from pydantic import BaseModel


class ConvertCurrencyRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class ConvertCurrencyResponse(BaseModel):
    conversion_rate: float
    conversion_result: float