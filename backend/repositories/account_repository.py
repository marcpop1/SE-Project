from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.account import Account
from models.user import User
from repositories.repository_base import RepositoryBase


class AccountRepository(RepositoryBase[Account]):
    def __init__(self, session: Session):
        super().__init__(Account, session)

    def find_all_by_user_id(self, user_id: int) -> list[Account]:
        return self.session \
            .query(Account) \
            .filter(Account.user_id == user_id) \
            .all()
    
    def find_one_by_user_id(self, user_id: int) -> Optional[Account]:
        account = self.session \
            .query(Account) \
            .filter(Account.user_id == user_id) \
            .first()
        
        if not account:
            raise HTTPException(status_code=404, detail=f"No account for user with id: {user_id}")
        
        return account
    
    def find_by_username(self, username: str) -> Optional[Account]:
        account = self.session \
            .query(Account) \
            .join(User, Account.user_id == User.id) \
            .filter(User.username == username) \
            .first()
        
        if not account:
             raise HTTPException(status_code=404, detail=f"No account for user with username: {username}")
         
        return account
