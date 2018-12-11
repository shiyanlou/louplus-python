from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, post_load

from .base import Base
from .user import UserSchema


class WalletTransaction(Base):
    __tablename__ = 'wallet_transaction'

    amount = Column(Integer, nullable=False)
    note = Column(String(200), nullable=False, default='')
    payer_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    payee_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    payer = relationship('User', uselist=False, foreign_keys=[
                         payer_id], backref=backref('payer_transactions', lazy='dynamic'))
    payee = relationship('User', uselist=False, foreign_keys=[
                         payee_id], backref=backref('payee_transactions', lazy='dynamic'))


class WalletTransactionSchema(Schema):
    id = fields.Int()
    amount = fields.Int()
    note = fields.Str()
    payer_id = fields.Int()
    payee_id = fields.Int()
    payer = fields.Nested(UserSchema)
    payee = fields.Nested(UserSchema)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_user(self, data):
        return WalletTransaction(**data)
