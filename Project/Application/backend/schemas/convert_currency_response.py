from pydantic import BaseModel


class ConvertCurrencyResponse(BaseModel):
    conversion_rate: float
    conversion_result: float