from repositories.account_repository import AccountRepository
from schemas.user_schemas import UserDetailsResponse
from models.transaction import Transaction
from shared.enums.transaction.transaction_status import TransactionStatus
from shared.enums.transaction.transaction_type import TransactionType
from repositories.transaction_repository import TransactionRepository
from schemas.transaction_schemas import AddMoneyRequest, CreateTransactionRequest


class TransactionService():
    def __init__(self, account_repository: AccountRepository, transaction_repository: TransactionRepository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def create_transaction(self, user: UserDetailsResponse, transaction: CreateTransactionRequest):
        account_from = self.account_repository.get_by_user_id(user.id)
        if not account_from:
            raise ValueError("Account not found for the given user_id")
        
        if account_from.balance < transaction.amount:
            raise ValueError("Not enough money")
        
        account_to = self.account_repository.get_by_username(transaction.account_to_username)

        account_from.balance -= transaction.amount
        account_to.balance += transaction.amount

        self.account_repository.update(account_from)
        self.account_repository.update(account_to)

        new_transaction = Transaction(
            account_from_id = account_from.id,
            account_to_id = account_to.id,
            amount = transaction.amount,
            currency = transaction.currency,
            status = TransactionStatus.COMPLETED,
            type = TransactionType.TRANSFER
        )

        return self.transaction_repository.add(new_transaction)
    
    def add_money(self, user: UserDetailsResponse, transaction: AddMoneyRequest):
        account = self.account_repository.get_by_user_id(user.id)
        if not account:
            raise ValueError("Account not found for the given user_id")
        
        account.balance += transaction.amount

        self.account_repository.update(account)

        new_transaction = Transaction(
            account_from_id = account.id,
            account_to_id = account.id,
            amount = transaction.amount,
            currency = "RON",
            status = TransactionStatus.COMPLETED,
            type = TransactionType.TOP_UP
        )

        return self.transaction_repository.add(new_transaction)

