from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm.session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
session = Session()
migrate = Migrate()


def init(app):
    global db, session, migrate

    db = SQLAlchemy(app)
    session = db.session
    migrate = Migrate(app, db)


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)
