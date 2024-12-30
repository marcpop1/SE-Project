from sqlalchemy.orm import Session

from accounts.models import Account
from shared.repositories import BaseRepository


class AccountRepository(BaseRepository[Account]):
    def __init__(self, session: Session):
        super().__init__(Account, session)
