from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root@localhost/shiyanlougithub')
session = sessionmaker(engine)()
Base = declarative_base(engine)

class Repository(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    update_time = Column(DateTime)


if __name__ == '__main__':
    Base.metadata.create_all()
