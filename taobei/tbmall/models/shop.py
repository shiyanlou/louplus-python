from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from .base import Base


class Shop(Base):
    __tablename__ = 'shop'
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
    )

    name = Column(String(200), nullable=False, unique=True)
    description = Column(String(2000), nullable=False, default='')
    cover = Column(String(200), nullable=False, default='')
    user_id = Column(Integer, nullable=False)


class ShopSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    cover = fields.Str()
    user_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_shop(self, data):
        return Shop(**data)
