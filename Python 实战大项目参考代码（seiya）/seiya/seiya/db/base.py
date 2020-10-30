from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root@localhost:3306/seiya?charset=utf8')
Base = declarative_base()
Session = sessionmaker(bind=engine)
