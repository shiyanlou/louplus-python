from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class AddressModel(BaseModel):
    __tablename__ = 'address'

    address = Column(String(100), nullable=False)
    zip_code = Column(String(6), nullable=False, default='')
    phone = Column(String(20), nullable=False)
    is_default = Column(Boolean, nullable=False, default=False)
    owner_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User', uselist=False, back_populates='addresses')
