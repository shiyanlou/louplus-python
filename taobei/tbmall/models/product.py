from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from .base import Base
from .shop_product import shop_product


class Product(Base):
    __tablename__ = 'product'

    title = Column(String(20), nullable=False)
    description = Column(String(200), nullable=False, default='')
    cover = Column(String(100), nullable=False, default='')
    price = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    shops = relationship('Shop', secondary=shop_product,
                         back_populates='products', lazy='dynamic')


class ProductSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    cover = fields.Str()
    price = fields.Int()
    amount = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_product(self, data):
        return Product(**data)
