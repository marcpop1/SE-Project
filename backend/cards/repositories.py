from sqlalchemy.orm import Session

from accounts.models import Account
from cards.models import Card
from shared.repositories import BaseRepository


class CardRepository(BaseRepository[Card]):

    def __init__(self, session: Session):
        super().__init__(Card, session)

    def find_all_by_user_id(self, user_id: int) -> list[Card]:
        predicate = Account.user_id == user_id
        return self.session.query(Card).join(Account).filter(predicate).all()
