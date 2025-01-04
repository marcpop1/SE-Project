from fastapi import HTTPException
from services.transaction_serializer_service import TransactionSerializerService
from shared.enums.currency import Currency
from schemas.currency_schemas import ConvertCurrencyRequest
from controllers.currency_controller import CurrencyController
from models.account import Account
from repositories.account_repository import AccountRepository
from models.transaction import Transaction
from schemas.user_schemas import UserDetailsResponse
from shared.enums.transaction.transaction_status import TransactionStatus
from shared.enums.transaction.transaction_type import TransactionType
from repositories.transaction_repository import TransactionRepository
from schemas.transaction_schemas import AddMoneyRequest, CreateTransactionRequest, TransactionResponse, UpdateTransactionRequest


class TransactionService:
    def __init__(self,
                 account_repository: AccountRepository,
                 transaction_repository: TransactionRepository,
                 transaction_serializer: TransactionSerializerService,
                 currency_controller: CurrencyController):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.transaction_serializer = transaction_serializer
        self.currency_controller = currency_controller

    def get_by_id(self, transaction_id: int, user: UserDetailsResponse) -> TransactionResponse:
        transaction = self.transaction_repository.find_by_id(id=transaction_id)
        return self.transaction_serializer.serialize_transaction(transaction, user.id)
    
    def retrieve_all_for_user(self, user_id: int) -> list[TransactionResponse]:
        transactions = self.transaction_repository.find_all_by_user_id(user_id)
        return [self.transaction_serializer.serialize_transaction(t, user_id) for t in transactions]

    def update_transaction(self, transaction_id: int, user: UserDetailsResponse, data: UpdateTransactionRequest) -> TransactionResponse:
        transaction_to_update = self.transaction_repository.find_one_by_user_id(transaction_id, user_id=user.id)
        
        for key, value in transaction_to_update.__dict__.items():
            setattr(transaction_to_update, key, value)
            
        updated_transaction = self.transaction_repository.update(entity=transaction_to_update)
        return TransactionResponse.model_validate(updated_transaction)
    
    def delete_transaction(self, transaction_id, user: UserDetailsResponse) -> None:
        transaction_to_delete = self.transaction_repository.find_one_by_user_id(transaction_id, user_id=user.id)        
        self.transaction_repository.delete(entity=transaction_to_delete)

    async def place_transaction_between_accounts(self, afrom: Account, ato: Account, data: CreateTransactionRequest) -> TransactionResponse:
        convert_currency_request = ConvertCurrencyRequest(
            from_currency=data.currency,
            to_currency=Currency.RON,
            amount=data.amount
        )

        conversion_response = await self.currency_controller.convert_currency(convert_currency_request)
        converted_amount = conversion_response.conversion_result

        if afrom.balance < converted_amount:
            raise HTTPException(status_code=422, detail="Insufficient funds in the source account")

        if afrom.id == ato.id:
            raise HTTPException(status_code=422, detail="Cannot send money to the same account")

        afrom.balance -= converted_amount
        ato.balance += converted_amount
        
        self.account_repository.update(entity=afrom)
        self.account_repository.update(entity=ato)

        transaction = Transaction(
            account_from_id = afrom.id,
            account_to_id = ato.id,
            amount = data.amount,
            currency = data.currency,
            converted_amount = converted_amount,
            rate = conversion_response.conversion_rate,
            status = TransactionStatus.COMPLETED,
            type = TransactionType.TRANSFER
        )
        
        placed_transaction = self.transaction_repository.save(entity=transaction)
        return TransactionResponse.model_validate(placed_transaction)
 
    def add_money(self, account: Account, data: AddMoneyRequest) -> TransactionResponse:
        account.balance += data.amount
        self.account_repository.update(account)

        new_transaction = Transaction(
            account_from_id = account.id,
            account_to_id = account.id,
            amount = data.amount,
            currency = Currency.RON.value,
            converted_amount = data.amount,
            rate = 1,
            status = TransactionStatus.COMPLETED,
            type = TransactionType.TOP_UP
        )

        transaction = self.transaction_repository.save(entity=new_transaction)
        return TransactionResponse.model_validate(transaction)
    
    def revert_transaction(self, transaction_id: int) -> TransactionResponse:
        transaction_to_revert = self.transaction_repository.find_by_id(id=transaction_id)
   
        if transaction_to_revert.status != TransactionStatus.COMPLETED:
            raise HTTPException(
                status_code=403,
                detail=f'Transaction {transaction_id} is not in completed status'
            )
   
        transfered_amount = transaction_to_revert.converted_amount
        
        afrom = transaction_to_revert.account_from
        ato = transaction_to_revert.account_to
        
        afrom.balance += transfered_amount
        ato.balance -= transfered_amount
        
        self.account_repository.update(entity=ato)
        self.account_repository.update(entity=afrom)
        
        transaction_to_revert.status = TransactionStatus.REVERTED 
        updated_transaction = self.transaction_repository.update(entity=transaction_to_revert)    
        
        return TransactionResponse.model_validate(updated_transaction)