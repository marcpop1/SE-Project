from datetime import timedelta, datetime
from fastapi import HTTPException
from models.user import User
from repositories.user_repository import UserRepository
from schemas.user_schemas import CreateUserRequest
from jose import jwt

class AuthenticationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def register_user(self, data: CreateUserRequest, bcrypt) -> None:
        hashed_password = bcrypt.hash(data.password)
        user_to_register = User(name=data.name, username=data.username, hashed_password=hashed_password)
        self.user_repository.save(user_to_register)
        
    def authenticate(self, username: str, password: str, bcrypt) -> User:
        user = self.user_repository.find_by_username(username)
        
        if not bcrypt.verify(password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Provided password is incorect')
        
        return user
    
    def create_access_token(self, user: User, key: str, alg: str, valid_period: timedelta = timedelta(days=1)) -> str:
        expires_at = datetime.utcnow() + valid_period
        
        jwt_payload = {
            'id': user.id,
            'sub': user.username,
            'name': user.name,
            'role': user.role.value,
            'exp': expires_at
        }
        
        return jwt.encode(jwt_payload, key, algorithm=alg)
        
        