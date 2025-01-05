from models.transaction import Transaction
from schemas.transaction_response import TransactionResponse


class TransactionSerializerController:
    def serialize_transaction(self, transaction: Transaction, user_id: int) -> TransactionResponse:
        if transaction.account_from.user.id == user_id and transaction.account_to.user.id != user_id:
            return TransactionResponse.model_validate(transaction).model_copy(update={"amount": -transaction.amount})
        return TransactionResponse.model_validate(transaction) 