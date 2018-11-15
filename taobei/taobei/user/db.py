from importlib import import_module

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = None
migrate = None


def init(app):
    global db, migrate

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    import_module('.models', __package__)
