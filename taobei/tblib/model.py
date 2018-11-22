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
