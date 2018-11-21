from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from tblib.model import Base


class FavoriteProduct(Base):
    __tablename__ = 'favorite_product'
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id'),
        Index('idx_product_id', 'product_id'),
    )

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
