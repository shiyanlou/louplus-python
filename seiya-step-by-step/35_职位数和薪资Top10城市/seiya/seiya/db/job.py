from sqlalchemy import Column, Integer, String
from .base import Base

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), index=True)
    city = Column(String(64), index=True)
    salary_low = Column(Integer)
    salary_up = Column(Integer)
    experience_low = Column(Integer)
    experience_up = Column(Integer)
    education = Column(String(32))
    tags = Column(String(128))
    company = Column(String(64))
