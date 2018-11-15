from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class WalletTransaction(Base):
    __tablename__ = 'wallet_transaction'

    amount = Column(Integer, nullable=False)
    note = Column(String(100), nullable=False, default='')
    payer_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    payee_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    payer = relationship(
        'User', uselist=False, back_populates='payer_transactions', foreign_keys=[payer_id])
    payee = relationship(
        'User', uselist=False, back_populates='payee_transactions', foreign_keys=[payee_id])
