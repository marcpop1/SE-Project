from fastapi import APIRouter, Depends
from schemas.account_schemas import AccountResponse, CreateAccountRequest, UpdateAccountRequest
from dependencies import get_account_service, get_current_user
from fastapi_restful.cbv import cbv
from schemas.user_schemas import UserDetailsResponse
from services.account_service import AccountService

router = APIRouter(
    prefix='/accounts',
    tags=['accounts']
)


@cbv(router)
class AccountController:
    user: UserDetailsResponse = Depends(get_current_user)
    account_service: AccountService = Depends(get_account_service)
    
    @router.post("/", response_model=AccountResponse, status_code=201)
    def create_account(self, payload: CreateAccountRequest):
        return self.account_service.add_new_account(data=payload)
    
    @router.get("/", response_model=list[AccountResponse])
    def list_accounts_for_user(self):
        return self.account_service.get_all_for_user(user=self.user)
    
    @router.get("/{account_id}", response_model=AccountResponse)
    def retrieve_account_by_id(self, account_id: int):
        return self.account_service.get_account_by_id(account_id)

    @router.put("/{account_id}", response_model=AccountResponse)
    def update_account(self, account_id: int, payload: UpdateAccountRequest):
        return self.account_service.update_account_by_id(account_id, data=payload)

    @router.delete("/{account_id}", status_code=204)
    def delete_account(self, account_id: int):
        self.account_service.remove_account_by_id(account_id)

    @router.get("/user/")
    def retrieve_first_by_user_id(self):
        return self.account_service.get_account_by_user_id(user=self.user)

    @router.get("/username/{username}", response_model=AccountResponse)
    def retrieve_by_username(self, username: str):
        return self.account_service.get_account_by_username(username)
