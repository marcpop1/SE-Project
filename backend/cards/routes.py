import datetime
import random
import string

from fastapi import APIRouter, HTTPException, Depends
from fastapi_restful.cbv import cbv

from accounts.models import Account
from cards.models import Card
from cards.schemas import CardDetailResponse, CreateCardRequest
from cards.services import CardService
from dependecies import db_dependency, user_dependency, LoggedUser, get_card_service

router = APIRouter(
    prefix='/cards',
    tags=['cards']
)


@cbv(router)
class CardController:
    card_service: CardService = Depends(get_card_service)

    @router.get("/v2", response_model=list[CardDetailResponse])
    def get_cards_for_user(self, user: LoggedUser):
        cards = self.card_service.find_cards_for_user(user)
        return cards

    @router.post("/v2", response_model=CardDetailResponse)
    def add_card_for_user(self, user: LoggedUser, payload: CreateCardRequest):
        card = self.card_service.create_new_card(user, data=payload)
        return CardDetailResponse.model_validate(card)


# @router.post("/", response_model=CardDetailResponse)
# async def create_card_for_user(db: db_dependency, payload: CreateCardRequest):
#     account = (db.query(Account)
#                .filter(Account.id == payload.account_id)
#                .first())
#
#     if not account:
#         raise HTTPException(status_code=404, detail=f"Account with id={payload.account_id} does not exist")
#
#     card_number, cvv = generate_card_number(), generate_cvv()
#
#     card_number = generate_card_number()
#     cvv = generate_cvv()
#     expiration_year, expiration_month = generate_card_expiration_date()
#
#     created_card = Card(
#         account_id=account.id,
#         holder_name=account.user.name,
#         number=card_number,
#         expiration_month=expiration_month,
#         expiration_year=expiration_year,
#         cvv=cvv,
#         type=payload.card_type,
#         currency=payload.card_currency,
#         is_primary=payload.is_primary
#     )
#
#     db.add(created_card)
#     db.commit()
#     db.refresh(created_card)
#
#     return CardDetailResponse.model_validate(created_card)
