from tblib.handler import handle_error

from .common import common
from .product import product
from .shop import shop
from .user import user


def init(app):
    if app.env == 'production':
        app.register_error_handler(Exception, handle_error)

    app.register_blueprint(common)
    app.register_blueprint(product)
    app.register_blueprint(shop)
    app.register_blueprint(user)
