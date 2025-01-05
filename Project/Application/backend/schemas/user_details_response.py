from pydantic import BaseModel


class UserDetailsResponse(BaseModel):
    id: int
    username: str
    name: str
    role: str

    class Config:
        from_attributes = True