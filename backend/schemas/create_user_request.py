from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    name: str
    username: str
    password: str
