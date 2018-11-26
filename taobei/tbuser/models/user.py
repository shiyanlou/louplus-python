from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, post_load

from .base import Base


class Gender:
    UNKNOWN = ''
    MALE = 'm'
    FEMALE = 'f'


class User(Base):
    __tablename__ = 'user'

    username = Column(String(20), nullable=False, unique=True)
    _password = Column('password', String(256), nullable=False)
    avatar = Column(String(200), nullable=False, default='')
    gender = Column(String(1), nullable=False, default=Gender.UNKNOWN)
    mobile = Column(String(11), unique=True)
    wallet_money = Column(Integer, nullable=False, default=0)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    avatar = fields.Str()
    gender = fields.Str()
    mobile = fields.Str()
    wallet_money = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_user(self, data):
        return User(**data)
