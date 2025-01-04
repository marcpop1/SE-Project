from fastapi import APIRouter, Depends
from schemas.user_schemas import UserDetailsResponse
from services.account_service import AccountService
from services.transaction_service import TransactionService
from schemas.transaction_schemas import AddMoneyRequest, TransactionResponse, CreateTransactionRequest, UpdateTransactionRequest
from dependencies import get_account_service, get_current_user, get_transaction_service
from fastapi_restful.cbv import cbv

router = APIRouter(
    prefix='/transactions',
    tags=['transactions']
)
        

@cbv(router)
class TransactionController:
    user: UserDetailsResponse = Depends(get_current_user)
    transaction_service: TransactionService = Depends(get_transaction_service)
    account_service: AccountService = Depends(get_account_service)
    
    @router.post("/", response_model=TransactionResponse, status_code=201)
    async def create_transaction(self, payload: CreateTransactionRequest):
        source_account = self.account_service.get_account_by_user_id(user_id=self.user.id)
        destination_account = self.account_service.get_account_by_username(username=payload.account_to_username)
        return await self.transaction_service.place_transaction_between_accounts(source_account, destination_account, payload)
    
    @router.get("/", response_model=list[TransactionResponse])
    def list_all_for_logged_user(self):
        return self.transaction_service.retrieve_all_for_user(user_id=self.user.id)
    
    @router.get('/{transaction_id}', response_model=TransactionResponse)
    def get_by_id(self, transaction_id: int):
        return self.transaction_service.get_by_id(transaction_id, self.user)
    
    @router.put('/{transaction_id}', response_model=TransactionResponse)
    def update(self, transaction_id: int, payload: UpdateTransactionRequest):
        return self.transaction_service.update_transaction(transaction_id, user=self.user, data=payload)
    
    @router.delete('/{transaction_id}', status_code=204)
    def delete(self, transaction_id):
        self.transaction_service.delete_transaction(transaction_id, user=self.user)
        
    @router.post('/add-money/', response_model=TransactionResponse, status_code=201)
    def add_money(self, payload: AddMoneyRequest):
        account_to_add = self.account_service.get_account_by_user_id(user_id=self.user.id)
        return self.transaction_service.add_money(account=account_to_add, data=payload)