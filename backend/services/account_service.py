from models.account import Account
from repositories.account_repository import AccountRepository
from schemas.account_schemas import AccountResponse, CreateAccountRequest, UpdateAccountRequest
from schemas.user_schemas import UserDetailsResponse


class AccountService:
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
        return account
    
    def get_account_by_user_id(self, user: UserDetailsResponse) -> Account:
        """Returns the first account for the specified user.id, HTTPException is raised if no account found"""
        
        account = self.account_repository.find_one_by_user_id(user_id=user.id)
        return account
    
    def get_account_by_username(self, username: str) -> Account:
        """Returns the first account for the specified user.username, HTTPException is raised if no account found"""
        
        account = self.account_repository.find_by_username(username)
        return account
    
    def update_account_by_id(self, account_id: int, data: UpdateAccountRequest) -> AccountResponse:
        account_to_update = self.account_repository.find_by_id(id=account_id)
        
        for key, value in data.__dict__.items():
            setattr(account_to_update, key, value)
        
        updated_account = self.account_repository.update(entity=account_to_update)
        return AccountResponse.model_validate(updated_account)
    
    def remove_account_by_id(self, account_id: int) -> None:
        account_to_delete = self.account_repository.find_by_id(id=account_id)
        self.account_repository.delete(entity=account_to_delete)