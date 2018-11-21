from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from tblib.model import db


shop_product = db.Table(
    'shop_product',
    Column('shop_id', Integer, ForeignKey('shop.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True)
)
