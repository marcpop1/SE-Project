from sqlalchemy import update
from sqlalchemy.orm import Session

from models.account import Account
from models.card import Card
from repositories.repository_base import RepositoryBase


class CardRepository(RepositoryBase[Card]):

    def __init__(self, session: Session):
        super().__init__(Card, session)

    def find_all_by_user_id(self, user_id: int) -> list[Card]:
        predicate = Account.user_id == user_id
        return self.session.query(Card).join(Account).filter(predicate).all()

    def update_primary_status_by_user_id(self, user_id: int, is_primary: bool = False) -> None:
        stmt = (
            update(Card)
            .where(Card.account_id == Account.id)
            .where(Account.user_id == user_id)
            .values(is_primary=False)
        )
        try:
            self.session.execute(stmt)
            self.session.commit()
        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
