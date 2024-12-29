import datetime
import random
import string

from fastapi import APIRouter, HTTPException

from account.models import Account
from cards.models import Card
from cards.schemas import CardDetailResponse, CreateCardRequest
from dependecies import db_dependency, user_dependency

router = APIRouter(
    prefix='/cards',
    tags=['cards']
)


@router.get("", response_model=list[CardDetailResponse])
def get_cards_for_user(db: db_dependency, user: user_dependency):
    cards = (db.query(Card)
             .join(Account)
             .filter(Account.user_id == user.get('id'))
             .all()
             )

    return cards


def generate_card_number() -> str:
    char_pool = ''.join([random.choice(string.digits + string.ascii_uppercase) for _ in range(16)])
    return ' '.join([char_pool[i:i + 4] for i in range(0, 16, 4)])


def generate_cvv() -> str:
    return ''.join([random.choice(string.digits) for _ in range(3)])


def generate_card_expiration_date(plus_year: int = 5, plus_month: int = 0) -> tuple[int, int]:
    now = datetime.datetime.now()
    return now.year + plus_year, now.month + plus_month


@router.post("/", response_model=CardDetailResponse)
async def create_card_for_user(db: db_dependency, payload: CreateCardRequest):
    account = (db.query(Account)
               .filter(Account.id == payload.account_id)
               .first())

    if not account:
        raise HTTPException(status_code=404, detail=f"Account with id={payload.account_id} does not exist")

    card_number, cvv = generate_card_number(), generate_cvv()

    card_number = generate_card_number()
    cvv = generate_cvv()
    expiration_year, expiration_month = generate_card_expiration_date()

    created_card = Card(
        account_id=account.id,
        holder_name=account.user.name,
        number=card_number,
        expiration_month=expiration_month,
        expiration_year=expiration_year,
        cvv=cvv,
        type=payload.card_type,
        currency=payload.card_currency,
        is_primary=payload.is_primary
    )

    db.add(created_card)
    db.commit()
    db.refresh(created_card)

    return CardDetailResponse.model_validate(created_card)
