import datetime
import random
import string

from fastapi import APIRouter, HTTPException, Depends
from fastapi_restful.cbv import cbv

from accounts.models import Account
from auth.schemas import UserDetailsResponse
from cards.models import Card
from cards.schemas import CardDetailResponse, CreateCardRequest, UpdateCardRequest
from cards.services import CardService
from dependecies import db_dependency, user_dependency, LoggedUser, get_card_service, get_current_user

router = APIRouter(
    prefix='/cards',
    tags=['cards']
)


@cbv(router)
class CardController:
    card_service: CardService = Depends(get_card_service)
    user: UserDetailsResponse = Depends(get_current_user)

    @router.get("/", response_model=list[CardDetailResponse])
    def get_cards_for_user(self):
        cards = self.card_service.find_cards_for_user(self.user)
        return cards

    @router.post("/", response_model=CardDetailResponse)
    def add_card_for_user(self, payload: CreateCardRequest):
        card = self.card_service.create_new_card(self.user, data=payload)
        return CardDetailResponse.model_validate(card)

    @router.put("/{card_id}", response_model=CardDetailResponse)
    def update_specified_card(self, card_id: int, payload: UpdateCardRequest):
        updated_card = self.card_service.update_card(self.user, card_id, data=payload)
        print(updated_card)
        return CardDetailResponse.model_validate(updated_card)

    @router.delete("/{card_id}", status_code=204)
    def remove_specified_card(self, card_id: int):
        self.card_service.remove_card_by_id(card_id)
