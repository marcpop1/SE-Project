from repositories.user_repository import UserRepository
from schemas.user_schemas import UserDetailsResponse


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def get_all_users(self) -> list[UserDetailsResponse]:
        users = self.user_repository.find_all()
        return [UserDetailsResponse.model_validate(user) for user in users]
    