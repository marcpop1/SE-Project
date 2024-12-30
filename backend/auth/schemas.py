from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    name: str
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserDetailsResponse(BaseModel):
    id: int
    username: str
    name: str
    role: str

    class Config:
        from_attributes = True