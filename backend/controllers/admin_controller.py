from typing import Optional
from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends, Query

from dependencies import get_transaction_service, get_user_service
from schemas.user_schemas import UserDetailsResponse
from services.transaction_service import TransactionService
from services.user_service import UserService

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


@cbv(router)
class AdminController:
    user_service: UserService = Depends(get_user_service)
    transaction_service: TransactionService = Depends(get_transaction_service)
    
    @router.get('/users', response_model=list[UserDetailsResponse])
    def list_all_users(self):
        pass
    
    @router.get('/transactions/{user_id}')
    def list_transactions(self, user_id: int):
        pass
    
    @router.put('/transactions/{transaction_id}/revert')
    def revert_specified_transaction(self):
        pass