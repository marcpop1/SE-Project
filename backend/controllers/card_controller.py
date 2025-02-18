import random
import string
import datetime

from fastapi import HTTPException

from repositories.account_repository import AccountRepository
from schemas.user_details_response import UserDetailsResponse
from models.card import Card
from repositories.card_repository import CardRepository
from schemas.create_card_request import CreateCardRequest


class CardController:
    def __init__(self, card_repository: CardRepository, account_repository: AccountRepository):
        self.card_repository = card_repository
        self.account_repository = account_repository

    def find_cards_for_user(self, user: UserDetailsResponse) -> list[Card]:
        cards = self.card_repository.find_all_by_user_id(user.id)
        if not cards:
            raise HTTPException(status_code=404, detail=f"User {user.id} does nto have any cards")
        return cards

    def create_new_card(self, user: UserDetailsResponse, data: CreateCardRequest) -> Card:
        associated_account = self.account_repository.find_one_by_user_id(user.id)

        new_card_number = self.__generate_card_number()
        new_cvv_code = self.__generate_cvv()

        expiration_year, expiration_month = self.__generate_card_expiration_date()

        new_card = Card(
            account_id=associated_account.id,
            holder_name=associated_account.user.name,
            number=new_card_number,
            expiration_month=expiration_month,
            expiration_year=expiration_year,
            cvv=new_cvv_code,
            type=data.type,
            currency=data.currency,
        )

        return self.card_repository.save(new_card)

    def __generate_card_number(self) -> str:
        char_pool = ''.join([random.choice(string.digits) for _ in range(16)])
        return ' '.join([char_pool[i:i + 4] for i in range(0, 16, 4)])

    def __generate_cvv(self) -> str:
        return ''.join([random.choice(string.digits) for _ in range(3)])

    def __generate_card_expiration_date(self, plus_year: int = 5, plus_month: int = 0) -> tuple[int, int]:
        now = datetime.datetime.now()
        return now.year + plus_year, now.month + plus_month

    def remove_card_by_id(self, card_id: int):
        card_to_remove = self.card_repository.find_by_id(card_id)
        self.card_repository.delete(card_to_remove)
