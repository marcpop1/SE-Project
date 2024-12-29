from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    balance = Column(Float)
    currency = Column(String)

    user = relationship("User", back_populates="accounts")
    cards = relationship("Card", back_populates="account")
    transactions_from = relationship("Transaction", foreign_keys="[Transaction.account_from_id]", back_populates="account_from")
    transactions_to = relationship("Transaction", foreign_keys="[Transaction.account_to_id]", back_populates="account_to")