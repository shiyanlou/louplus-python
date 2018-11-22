from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, post_load

from .base import Base
from .product import ProductSchema


class FavoriteProduct(Base):
    __tablename__ = 'favorite_product'
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id'),
        Index('idx_product_id', 'product_id'),
    )

    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey(
        'product.id', ondelete='CASCADE'), nullable=False)
    product = relationship('Product', uselist=False,
                           backref=backref('favorites', lazy='dynamic'))


class FavoriteProductSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    product_id = fields.Int()
    product = fields.Nested(ProductSchema)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_favorite_product(self, data):
        return FavoriteProduct(**data)
