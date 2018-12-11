from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from tblib.model import db


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
