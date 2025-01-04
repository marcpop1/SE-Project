from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends

from controllers.account_controller import AccountController
from dependencies import get_account_controller, get_current_user, get_transaction_controller, get_user_controller
from schemas.account_response import AccountResponse
from schemas.transaction_response import TransactionResponse
from schemas.user_details_response import UserDetailsResponse
from controllers.transaction_controller import TransactionController
from controllers.user_controller import UserController
from shared.decorators.authorize import authorize
from shared.enums.user.user_role import UserRole

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


@cbv(router)
class AdminView:
    user_controller: UserController = Depends(get_user_controller)
    account_controller: AccountController = Depends(get_account_controller)
    transaction_controller: TransactionController = Depends(get_transaction_controller)
    user: UserDetailsResponse = Depends(get_current_user)
        
    @router.get('/users', response_model=list[UserDetailsResponse])
    @authorize(roles=[UserRole.ADMIN])
    def list_all_users(self):
        return self.user_controller.get_all_users()
    
    @router.get("/account/{user_id}", response_model=AccountResponse)
    @authorize(roles=[UserRole.ADMIN])
    def retrieve_by_user_id(self, user_id: int):
        return self.account_controller.get_account_by_user_id(user_id)
    
    @router.get('/transactions/{user_id}', response_model=list[TransactionResponse])
    @authorize(roles=[UserRole.ADMIN])
    def list_transactions_made_by_user(self, user_id: int):
        return self.transaction_controller.retrieve_all_for_user(user_id)
    
    @router.put('/transactions/{transaction_id}/revert')
    @authorize(roles=[UserRole.ADMIN])
    def revert_specified_transaction(self, transaction_id: int):
        self.transaction_controller.revert_transaction(transaction_id)