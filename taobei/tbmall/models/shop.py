from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from tblib.model import Base

from .shop_product import shop_product


class Shop(Base):
    __tablename__ = 'shop'
    __table_args__ = (
        Index('idx_owner_id', 'owner_id'),
    )

    name = Column(String(20), nullable=False, unique=True)
    description = Column(String(200), nullable=False, default='')
    cover = Column(String(100), nullable=False, default='')
    owner_id = Column(Integer, nullable=False)
    products = relationship(
        'Product', secondary=shop_product, back_populates='shops', lazy='dynamic')


class ShopSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    cover = fields.Str()
    owner_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_shop(self, data):
        return Shop(**data)
