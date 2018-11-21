from tblib.handler import handle_error

from .shop import shop
from .product import product
from .favorite_product import favorite_product


def init(app):
    if app.env == 'production':
        app.register_error_handler(Exception, handle_error)

    app.register_blueprint(shop)
    app.register_blueprint(product)
    app.register_blueprint(favorite_product)
