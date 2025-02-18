from models.account import Account
from repositories.account_repository import AccountRepository
from schemas.account_response import AccountResponse
from schemas.create_account_request import CreateAccountRequest
from schemas.user_details_response import UserDetailsResponse


class AccountController:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository
        
    def add_new_account(self, data: CreateAccountRequest) -> AccountResponse:
        account_to_create = Account(**data.__dict__)
        created_account = self.account_repository.save(account_to_create)
        return AccountResponse.model_validate(created_account)
    
    def get_all_for_user(self, user: UserDetailsResponse) -> list[AccountResponse]:
        """Returns all accounts for the specifed user"""
        
        accounts = self.account_repository.find_all_by_user_id(user_id=user.id) 
        return [AccountResponse.model_validate(account) for account in accounts]
    
    def get_account_by_id(self, account_id: int) -> Account:
        """Returns the account with the coresponding id, HTTPException is raised if no account found"""
        
        account = self.account_repository.find_by_id(id=account_id)
        account.balance = round(account.balance, 2)
        return account
    
    def get_account_by_user_id(self, user_id: int) -> Account:
        """Returns the first account for the specified user.id, HTTPException is raised if no account found"""
        
        account = self.account_repository.find_one_by_user_id(user_id=user_id)
        account.balance = round(account.balance, 2)
        return account
    
    def get_account_by_username(self, username: str) -> Account:
        """Returns the first account for the specified user.username, HTTPException is raised if no account found"""
        
        account = self.account_repository.find_by_username(username)
        account.balance = round(account.balance, 2)
        return account
    
    def remove_account_by_id(self, account_id: int) -> None:
        account_to_delete = self.account_repository.find_by_id(id=account_id)
        self.account_repository.delete(entity=account_to_delete)