from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from .base import Base


class FavoriteProduct(Base):
    __tablename__ = 'favorite_product'

    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey(
        'product.id', ondelete='CASCADE'), nullable=False)


class FavoriteProductSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    product_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_favorite_product(self, data):
        return FavoriteProduct(**data)
