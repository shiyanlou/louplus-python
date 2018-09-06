from sqlalchemy import Column, String, Integer

from seiya.db.base import Base


class JobModel(Base):
    """职位 Model

    """
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    city = Column(String(16))
    salary_lower = Column(Integer)
    salary_upper = Column(Integer)
    experience_lower = Column(Integer)
    experience_upper = Column(Integer)
    education = Column(String(16))
    tags = Column(String(256))
    company = Column(String(32))
