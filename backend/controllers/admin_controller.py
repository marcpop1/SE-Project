from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends

from dependencies import get_current_user, get_transaction_service, get_user_service
from schemas.transaction_schemas import TransactionResponse
from schemas.user_schemas import UserDetailsResponse
from services.transaction_service import TransactionService
from services.user_service import UserService
from shared.decorators.authorize import authorize
from shared.enums.user.user_role import UserRole

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


@cbv(router)
class AdminController:
    user_service: UserService = Depends(get_user_service)
    transaction_service: TransactionService = Depends(get_transaction_service)
    user: UserDetailsResponse = Depends(get_current_user)
        
    @router.get('/users', response_model=list[UserDetailsResponse])
    @authorize(roles=[UserRole.ADMIN])
    def list_all_users(self):
        return self.user_service.get_all_users()
    
    @router.get('/transactions/{user_id}', response_model=list[TransactionResponse])
    @authorize(roles=[UserRole.ADMIN])
    def list_transactions_made_by_user(self, user_id: int):
        return self.transaction_service.retrieve_all_for_user(user_id)
    
    @router.put('/transactions/{transaction_id}/revert')
    @authorize(roles=[UserRole.ADMIN])
    def revert_specified_transaction(self, transaction_id: int):
        self.transaction_service.revert_transaction(transaction_id)