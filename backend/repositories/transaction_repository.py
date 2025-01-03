from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session, aliased
from models.account import Account
from models.transaction import Transaction
from repositories.repository_base import RepositoryBase


class TransactionRepository(RepositoryBase[Transaction]):
    def __init__(self, session: Session):
        super().__init__(Account, session)


    def find_all_by_user_id(self, user_id: int) -> list[Transaction]:
        account_from = aliased(Account)
        account_to = aliased(Account)

        return self.session \
            .query(Transaction) \
            .join(account_from, Transaction.account_from_id == account_from.id) \
            .join(account_to, Transaction.account_to_id == account_to.id) \
            .filter((account_from.user_id == user_id) | (account_to.user_id == user_id)) \
            .order_by(desc(Transaction.created_at)) \
            .all() 
            
    def find_one_by_user_id(self, transaction_id: int, user_id: int) -> Transaction:
        account_from = aliased(Account)
        account_to = aliased(Account)

        transaction = self.session.query(Transaction) \
                       .join(account_from, Transaction.account_from_id == Account.id) \
                       .join(account_to, Transaction.account_to_id == Account.id) \
                       .filter(Transaction.id == transaction_id, Account.user_id == user_id) \
                       .first()

        if not transaction:
            raise HTTPException(
                status_code=404,
                detail=f"No transaction with transactionId={transaction_id} and userId={user_id} found"
                )
        
        return transaction