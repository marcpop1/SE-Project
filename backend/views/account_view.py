from fastapi import APIRouter, Depends
from schemas.account_response import AccountResponse
from schemas.create_account_request import CreateAccountRequest
from dependencies import get_account_controller, get_current_user
from fastapi_restful.cbv import cbv
from schemas.user_details_response import UserDetailsResponse
from controllers.account_controller import AccountController

router = APIRouter(
    prefix='/accounts',
    tags=['accounts']
)


@cbv(router)
class AccountView:
    user: UserDetailsResponse = Depends(get_current_user)
    account_controller: AccountController = Depends(get_account_controller)
    
    @router.post("/", response_model=AccountResponse, status_code=201)
    def create_account(self, payload: CreateAccountRequest):
        return self.account_controller.add_new_account(data=payload)
    
    @router.get("/", response_model=list[AccountResponse])
    def list_accounts_for_user(self):
        return self.account_controller.get_all_for_user(user=self.user)
    
    @router.get("/{account_id}", response_model=AccountResponse)
    def retrieve_account_by_id(self, account_id: int):
        return self.account_controller.get_account_by_id(account_id)

    @router.delete("/{account_id}", status_code=204)
    def delete_account(self, account_id: int):
        self.account_controller.remove_account_by_id(account_id)

    @router.get("/user/")
    def retrieve_first_by_user_id(self):
        return self.account_controller.get_account_by_user_id(user_id=self.user.id)

    @router.get("/username/{username}", response_model=AccountResponse)
    def retrieve_by_username(self, username: str):
        return self.account_controller.get_account_by_username(username)
