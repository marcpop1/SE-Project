import random
import string
import datetime

from fastapi import HTTPException

from repositories.account_repository import AccountRepository
from schemas.user_schemas import UserDetailsResponse
from models.card import Card
from repositories.card_repository import CardRepository
from schemas.card_schemas import CreateCardRequest, UpdateCardRequest


def generate_card_number() -> str:
    char_pool = ''.join([random.choice(string.digits) for _ in range(16)])
    return ' '.join([char_pool[i:i + 4] for i in range(0, 16, 4)])


def generate_cvv() -> str:
    return ''.join([random.choice(string.digits) for _ in range(3)])


def generate_card_expiration_date(plus_year: int = 5, plus_month: int = 0) -> tuple[int, int]:
    now = datetime.datetime.now()
    return now.year + plus_year, now.month + plus_month


class CardService:
    def __init__(self, card_repository: CardRepository, account_repository: AccountRepository):
        self.card_repository = card_repository
        self.account_repository = account_repository

    def find_cards_for_user(self, user: UserDetailsResponse) -> list[Card]:
        cards = self.card_repository.find_all_by_user_id(user.id)
        if not cards:
            raise HTTPException(status_code=404, detail=f"User {user.id} does nto have any cards")
        return cards

    def create_new_card(self, user: UserDetailsResponse, data: CreateCardRequest) -> Card:
        associated_account = self.account_repository.find_by_id(data.account_id)

        new_card_number = generate_card_number()
        new_cvv_code = generate_cvv()

        expiration_year, expiration_month = generate_card_expiration_date()

        new_card = Card(
            account_id=associated_account.id,
            holder_name=associated_account.user.name,
            number=new_card_number,
            expiration_month=expiration_month,
            expiration_year=expiration_year,
            cvv=new_cvv_code,
            type=data.card_type,
            currency=data.card_currency,
            is_primary=data.is_primary
        )

        return self.card_repository.save(new_card)

    def update_card(self, user: UserDetailsResponse, card_id: int, data: UpdateCardRequest) -> Card:
        if data.is_primary:
            self.card_repository.update_primary_status_by_user_id(user.id)

        card_to_update = self.card_repository.find_by_id(card_id)
        card_to_update.is_primary = data.is_primary
        card_to_update.currency = data.card_currency

        updated_card = self.card_repository.update(card_to_update)
        if not updated_card:
            raise HTTPException(status_code=500, detail=f"Failed to update card {card_id}")

        return updated_card

    def remove_card_by_id(self, card_id: int):
        card_to_remove = self.card_repository.find_by_id(card_id)
        self.card_repository.delete(card_to_remove)
