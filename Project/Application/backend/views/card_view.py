from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from schemas.create_card_request import CreateCardRequest
from schemas.user_details_response import UserDetailsResponse
from schemas.card_response import CardResponse
from controllers.card_controller import CardController
from dependencies import get_card_controller, get_current_user

router = APIRouter(
    prefix='/cards',
    tags=['cards']
)


@cbv(router)
class CardView:
    card_controller: CardController = Depends(get_card_controller)
    user: UserDetailsResponse = Depends(get_current_user)

    @router.get("/", response_model=list[CardResponse])
    def get_cards_for_user(self):
        cards = self.card_controller.find_cards_for_user(self.user)
        return cards

    @router.post("/", response_model=CardResponse)
    def add_card_for_user(self, payload: CreateCardRequest):
        card = self.card_controller.create_new_card(self.user, data=payload)
        return CardResponse.model_validate(card)

    @router.delete("/{card_id}", status_code=204)
    def remove_specified_card(self, card_id: int):
        self.card_controller.remove_card_by_id(card_id)
        return
