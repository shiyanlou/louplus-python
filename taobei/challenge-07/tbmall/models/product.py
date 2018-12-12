from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, post_load

from .base import Base
from .shop import ShopSchema


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = (
        Index('idx_shop_id', 'shop_id'),
    )

    title = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=False, default='')
    cover = Column(String(200), nullable=False, default='')
    price = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    shop_id = Column(Integer, ForeignKey(
        'shop.id', ondelete='CASCADE'), nullable=False)
    shop = relationship('Shop', uselist=False,
                        backref=backref('products', lazy='dynamic'))


class ProductSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    cover = fields.Str()
    price = fields.Int()
    amount = fields.Int()
    shop_id = fields.Int()
    shop = fields.Nested(ShopSchema)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_product(self, data):
        return Product(**data)
