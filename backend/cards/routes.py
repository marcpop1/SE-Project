from fastapi import APIRouter, HTTPException

from account.models import Account
from cards.models import Card
from cards.schemas import CardDetailResponse
from dependecies import db_dependency, user_dependency

router = APIRouter(
    prefix='/cards',
    tags=['cards']
)


@router.get("/", response_model=list[CardDetailResponse])
def get_cards_for_user(db: db_dependency, user: user_dependency):
    cards = (db.query(Card)
             .join(Account)
             .filter(Account.user_id == user.get('id'))
             .all()
             )

    return cards
