from datetime import datetime
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import text

from ..db import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
