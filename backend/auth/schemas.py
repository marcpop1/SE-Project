from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserDetailsResponse(BaseModel):
    id: int
    username: str
    name: str

    class Config:
        from_attributes = True