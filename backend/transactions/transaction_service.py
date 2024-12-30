from accounts.account_repository import AccountRepository
from auth.schemas import UserDetailsResponse
from transactions.transaction_repository import TransactionRepository
from transactions.models import Transaction
from .schemas import CreateTransactionRequest


class TransactionService():
    def __init__(self, account_repository: AccountRepository, transaction_repository: TransactionRepository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def create_transaction(self, user: UserDetailsResponse, transaction: CreateTransactionRequest):
        account_from = self.account_repository.get_by_user_id(user.id)
        if not account_from:
            raise ValueError("Account not found for the given user_id")
        
        account_to = self.account_repository.get_by_username(transaction.account_to_username)
        new_transaction = Transaction(
            account_from_id = account_from.id,
            account_to_id = account_to.id,
            amount = transaction.amount,
            currency = transaction.currency
        )

        return self.transaction_repository.add(new_transaction)

