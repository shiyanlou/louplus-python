from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from .base import Base


class CartProduct(Base):
    __tablename__ = 'cart_product'
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id'),
        Index('idx_product_id', 'product_id'),
    )

    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False, default=1)


class CartProductSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    product_id = fields.Int()
    amount = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_cart_product(self, data):
        return CartProduct(**data)
