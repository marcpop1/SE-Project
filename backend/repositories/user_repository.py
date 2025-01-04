from fastapi import HTTPException
from models.user import User
from repositories.repository_base import RepositoryBase


class UserRepository(RepositoryBase[User]):
    def __init__(self, session):
        super().__init__(User, session)
    
    def find_by_username(self, username: str) -> User:
        user = self.session.query(User) \
                .filter(User.username == username) \
                .first()
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User with username: {username} does no exist")
        
        return user