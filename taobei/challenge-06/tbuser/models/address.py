from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, post_load

from .base import Base
from .user import UserSchema


class Address(Base):
    __tablename__ = 'address'

    address = Column(String(200), nullable=False)
    zip_code = Column(String(6), nullable=False, default='')
    phone = Column(String(20), nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', uselist=False,
                        backref=backref('addresses', lazy='dynamic'))


class AddressSchema(Schema):
    id = fields.Int()
    address = fields.Str()
    zip_code = fields.Str()
    phone = fields.Str()
    is_default = fields.Bool()
    user_id = fields.Int()
    user = fields.Nested(UserSchema)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_user(self, data):
        return Address(**data)
