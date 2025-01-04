import os
from dotenv import load_dotenv
from fastapi_restful.cbv import cbv

from fastapi import APIRouter, HTTPException, Query
import httpx

from schemas.convert_currency_request import ConvertCurrencyRequest
from schemas.convert_currency_response import ConvertCurrencyResponse

router = APIRouter(prefix="/currency", tags=["currency"])


load_dotenv()

CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
CURRENCY_API_URL = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/pair"


@cbv(router)
class CurrencyView:
    @router.post("/convert")
    async def convert_currency(self, request: ConvertCurrencyRequest):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{CURRENCY_API_URL}/{request.from_currency}/{request.to_currency}/{request.amount}"
                )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to fetch exchange rates",
                )

            data = response.json()

            response = ConvertCurrencyResponse(
                conversion_rate=float(data["conversion_rate"]),
                conversion_result=float(data["conversion_result"]),
            )

            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
