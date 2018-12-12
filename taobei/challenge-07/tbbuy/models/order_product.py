from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, post_load

from .base import Base


class OrderProduct(Base):
    __tablename__ = 'order_product'
    __table_args__ = (
        UniqueConstraint('order_id', 'product_id'),
        Index('idx_product_id', 'product_id'),
    )

    order_id = Column(Integer, ForeignKey(
        'order.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False, default=1)
    order = relationship('Order', uselist=False, backref=backref(
        'order_products', lazy='dynamic'))


class OrderProductSchema(Schema):
    id = fields.Int()
    order_id = fields.Int()
    product_id = fields.Int()
    price = fields.Int()
    amount = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_order_product(self, data):
        return OrderProduct(**data)
