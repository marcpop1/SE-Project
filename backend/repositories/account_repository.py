from typing import List, Optional
from sqlalchemy.orm import Session
from models.account import Account
from schemas.account_schemas import AccountResponse
from models.user import User

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, account: Account) -> AccountResponse:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return AccountResponse.model_validate(account)

    def get_all(self, user_id: int) -> List[AccountResponse]:
        accounts = self.db.query(Account).filter(Account.user_id == user_id).all()
        return [AccountResponse.model_validate(account) for account in accounts]

    def get_by_user_id(self, user_id: int) -> Optional[Account]:
        account = self.db.query(Account).filter(Account.user_id == user_id).first()
        if account:
            return account
        return None
    
    def get_by_username(self, username: str) -> Optional[Account]:
        account = (self.db.query(Account)
                   .join(User, Account.user_id == User.id)
                   .filter(User.username == username)
                   .first())
        if account:
            return account
        return None

    def get_by_id(self, account_id: int) -> Optional[AccountResponse]:
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if account:
            return AccountResponse.model_validate(account)
        return None

    def update(self, account: Account) -> AccountResponse:
        self.db.commit()
        self.db.refresh(account)
        return AccountResponse.model_validate(account)

    def delete(self, account: Account) -> None:
        self.db.delete(account)
        self.db.commit()