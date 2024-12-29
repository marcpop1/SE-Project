from typing import List, Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session
from .models import Transaction
from accounts.models import Account
from .schemas import TransactionResponse

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, transaction: Transaction) -> TransactionResponse:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return TransactionResponse.model_validate(transaction)

    def get_all(self, user_id: int) -> List[TransactionResponse]:
        transactions = (self.db.query(Transaction)
                        .join(Account, (Transaction.account_from_id == Account.id) | (Transaction.account_to_id == Account.id))
                        .filter(Account.user_id == user_id)
                        .order_by(desc(Transaction.created_at))
                        .all())
        return [self._convert_to_response(transaction, user_id) for transaction in transactions]

    def get_by_id(self, transaction_id: int, user_id: int) -> Optional[TransactionResponse]:
        transaction = (self.db.query(Transaction)
                       .join(Account, (Transaction.account_from_id == Account.id) | (Transaction.account_to_id == Account.id))
                       .filter(Transaction.id == transaction_id, Account.user_id == user_id)
                       .first())
        if transaction:
            return self._convert_to_response(transaction, user_id)
        return None

    def update(self, transaction: Transaction) -> TransactionResponse:
        self.db.commit()
        self.db.refresh(transaction)
        return TransactionResponse.model_validate(transaction)

    def delete(self, transaction: Transaction) -> None:
        self.db.delete(transaction)
        self.db.commit()

    def _convert_to_response(self, transaction: Transaction, user_id: int) -> TransactionResponse:
        response = TransactionResponse.model_validate(transaction)
        if response.account_from_id == user_id:
            response.amount = -response.amount
        return response