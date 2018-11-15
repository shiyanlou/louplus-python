from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class WalletTransactionModel(BaseModel):
    __tablename__ = 'wallet_transaction'

    amount = Column(Integer, nullable=False)
    note = Column(String(100), nullable=False, default='')
    payer_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    payee_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    payer = relationship('User', uselist=False, foreign_keys=[payer_id],
                         back_populates='payer_transactions')
    payee = relationship('User', uselist=False, foreign_keys=[payee_id],
                         back_populates='payee_transactions')
