from fastapi import APIRouter, Depends
from schemas.add_money_request import AddMoneyRequest
from schemas.create_transaction_request import CreateTransactionRequest
from schemas.user_details_response import UserDetailsResponse
from controllers.account_controller import AccountController
from controllers.transaction_controller import TransactionController
from schemas.transaction_response import TransactionResponse
from dependencies import get_account_controller, get_current_user, get_transaction_controller
from fastapi_restful.cbv import cbv

router = APIRouter(
    prefix='/transactions',
    tags=['transactions']
)
        

@cbv(router)
class TransactionView:
    user: UserDetailsResponse = Depends(get_current_user)
    transaction_controller: TransactionController = Depends(get_transaction_controller)
    account_controller: AccountController = Depends(get_account_controller)
    
    @router.post("/", response_model=TransactionResponse, status_code=201)
    async def create_transaction(self, payload: CreateTransactionRequest):
        source_account = self.account_controller.get_account_by_user_id(user_id=self.user.id)
        destination_account = self.account_controller.get_account_by_username(username=payload.account_to_username)
        return await self.transaction_controller.place_transaction_between_accounts(source_account, destination_account, payload)
    
    @router.get("/", response_model=list[TransactionResponse])
    def list_all_for_logged_user(self):
        return self.transaction_controller.retrieve_all_for_user(user_id=self.user.id)
    
    @router.get('/{transaction_id}', response_model=TransactionResponse)
    def get_by_id(self, transaction_id: int):
        return self.transaction_controller.get_by_id(transaction_id, self.user)
    
    @router.delete('/{transaction_id}', status_code=204)
    def delete(self, transaction_id):
        self.transaction_controller.delete_transaction(transaction_id, user=self.user)
        
    @router.post('/add-money/', response_model=TransactionResponse, status_code=201)
    def add_money(self, payload: AddMoneyRequest):
        account_to_add = self.account_controller.get_account_by_user_id(user_id=self.user.id)
        return self.transaction_controller.add_money(account=account_to_add, data=payload)