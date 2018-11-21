from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, post_load

from tblib.model import Base


class OrderStatus:
    NEW = 'new'
    CANCELLED = 'cancelled'
    PAIED = 'paied'
    DELIVERED = 'delivered'
    RETURNED = 'returned'
    COMMENTED = 'commented'


class Order(Base):
    __tablename__ = 'order'
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
    )

    pay_amount = Column(Integer, nullable=False)
    note = Column(String(100), nullable=False, default='')
    address_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default=OrderStatus.NEW)
    order_products = relationship('OrderProduct', back_populates='order')


class OrderSchema(Schema):
    id = fields.Int()
    pay_amount = fields.Int()
    note = fields.Str()
    address_id = fields.Int()
    user_id = fields.Int()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_load
    def make_order(self, data):
        return Order(**data)
