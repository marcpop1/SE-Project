from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    name: str
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_role: str

class UserDetailsResponse(BaseModel):
    id: int
    username: str
    name: str
    role: str

    class Config:
        from_attributes = True