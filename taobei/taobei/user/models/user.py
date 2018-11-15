from enum import Enum

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from .base import BaseModel


class Gender(Enum):
    UNKNOWN = ''
    MALE = 'm'
    FEMALE = 'f'


class UserModel(BaseModel):
    __tablename__ = 'user'

    username = Column(String(20), nullable=False, unique=True)
    _password = Column('password', String(256), nullable=False)
    avatar = Column(String(100), nullable=False, default='')
    gender = Column(String(1), nullable=False, default=Gender.UNKNOWN)
    mobile = Column(String(11), unique=True)
    wallet_money = Column(Integer, nullable=False, default=0)
    addresses = relationship('Address', back_populates='owner')
    payer_transactions = relationship(
        'WalletTransaction', back_populates='payer')
    payee_transactions = relationship(
        'WalletTransaction', back_populates='payee')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)
