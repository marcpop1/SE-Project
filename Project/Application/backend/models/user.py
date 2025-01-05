from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from shared.enums.user.user_role import UserRole
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USER)

    accounts = relationship("Account", back_populates="user")
