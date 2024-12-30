from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    account_from_id = Column(Integer, ForeignKey('accounts.id'), index=True)
    account_to_id = Column(Integer, ForeignKey('accounts.id'), index=True)
    amount = Column(Float)
    currency = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    
    account_from = relationship("Account", foreign_keys=[account_from_id], back_populates="transactions_from")
    account_to = relationship("Account", foreign_keys=[account_to_id], back_populates="transactions_to")