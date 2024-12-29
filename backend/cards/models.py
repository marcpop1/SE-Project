from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), index=True)
    card_holder_name = Column(String)
    card_number = Column(String(16))
    expiration_month = Column(Integer, CheckConstraint('expiration_month >= 1 AND expiration_month <= 12'))
    expiration_year = Column(Integer, CheckConstraint('expiration_year >= 2000 AND expiration_year <= 2100'))
    cvv = Column(String(3))
    card_type = Column(String)
    card_currency = Column(String)
    is_primary = Column(Boolean)

    account = relationship("Account", back_populates="cards")