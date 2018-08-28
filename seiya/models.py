from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    'mysql://root@localhost:3306/data-analysis-project?charset=utf8')
Base = declarative_base()


class JobModel(Base):
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
