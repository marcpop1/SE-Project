from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from schemas.user_schemas import UserDetailsResponse
from schemas.card_schemas import CardDetailResponse, CreateCardRequest
from services.card_service import CardService
from dependencies import get_card_service, get_current_user

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

    @router.delete("/{card_id}", status_code=204)
    def remove_specified_card(self, card_id: int):
        self.card_service.remove_card_by_id(card_id)
        return
