from sqlalchemy.orm import Session

from models.account import Account
from repositories.repository_base import RepositoryBase


class AccountRepository(RepositoryBase[Account]):
    def __init__(self, session: Session):
        super().__init__(Account, session)
