from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from tblib.model import Base


class Address(Base):
    __tablename__ = 'address'

    address = Column(String(100), nullable=False)
    zip_code = Column(String(6), nullable=False, default='')
    phone = Column(String(20), nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)
    owner_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User', uselist=False, back_populates='addresses')


class AddressSchema(Schema):
    id = fields.Int()
    address = fields.Str()
    zip_code = fields.Str()
    phone = fields.Str()
    is_default = fields.Bool()
    owner_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_user(self, data):
        return Address(**data)
